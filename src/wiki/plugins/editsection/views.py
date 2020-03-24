import re

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy
from wiki import models
from wiki.core.markdown import article_markdown
from wiki.core.plugins.registry import get_markdown_extensions
from wiki.decorators import get_article
from wiki.plugins.editsection.markdown_extensions import EditSectionExtension
from wiki.views.article import Edit as EditView

from . import settings

ERROR_SECTION_CHANGED = gettext_lazy(
    "Unable to find the selected section. The article was modified meanwhile."
)
ERROR_SECTION_UNSAVED = gettext_lazy(
    "Your changes must be re-applied in the new section structure of the " "article."
)
ERROR_ARTICLE_CHANGED = gettext_lazy(
    "Unable to find the selected section in the current article. The article "
    "was changed in between. Your changed section is still available as the "
    "last now inactive revision of this article."
)
ERROR_TRY_AGAIN = gettext_lazy("Please try again.")


class FindHeader:
    """Locate the start, header text, and end of the header text of the next
    possible section starting from pos. Finds too many occurrences for SeText
    headers which are filtered out later in the markdown extension.
    Returns: start pos header sure_header level"""

    SETEXT_RE_TEXT = r"(?P<header1>.*?)\n(?P<level1>[=-])+[ ]*(\n|$)"
    SETEXT_RE = re.compile(r"\n%s" % SETEXT_RE_TEXT, re.MULTILINE)
    HEADER_RE = re.compile(
        r"((\A ?\n?|\n(?![^\n]{0,3}\w).*?\n)%s"
        r"|(\A|\n)(?P<level2>#{1,6})(?P<header2>.*?)#*(\n|$))" % SETEXT_RE_TEXT,
        re.MULTILINE,
    )
    ATTR_RE = re.compile(r"[ ]+\{\:?([^\}\n]*)\}[ ]*$")

    def __init__(self, text, pos):
        self.sure_header = False
        match = self.SETEXT_RE.match(text, pos)
        if match:
            self.sure_header = True
        else:
            match = self.HEADER_RE.search(text, pos)
            if not match:
                self.start = len(text) + 1
                self.pos = self.start
                return
        self.pos = match.end() - 1

        # Get level and header text of the section
        token = match.group("level1")
        if token:
            self.header = match.group("header1").strip()
            self.start = match.start("header1")
        else:
            token = match.group("level2")
            self.header = match.group("header2").strip()
            self.start = match.start("level2")
            self.sure_header = True
        # Remove attribute definitions from the header text
        match = self.ATTR_RE.search(self.header)
        if match:
            self.header = self.header[: match.start()].rstrip("#").rstrip()
        # Get level of the section
        if token[0] == "=":
            self.level = 1
        elif token[0] == "-":
            self.level = 2
        else:
            self.level = len(token)


class EditSection(EditView):
    def locate_section(self, article, text):
        """Search for the header self.location (which is not deeper than settings.MAX_LEVEL)
        in text, compare the header text with self.header_id, and return the start position
        and the end position+1 of the complete section started by the header.
        """
        text = text.replace("\r\n", " \n").replace("\r", "\n") + "\n\n"
        text_len = len(text)

        headers = []
        pos = 0
        while pos < text_len:
            # Get meta information and start position of the next section
            header = FindHeader(text, pos)
            pos = header.pos
            if pos >= text_len:
                break
            if header.level > settings.MAX_LEVEL:
                continue
            headers.append(header)

        for e in get_markdown_extensions():
            if isinstance(e, EditSectionExtension):
                e.config["headers"] = headers
                e.config["location"] = self.location
                e.config["header_id"] = self.header_id
                article_markdown(text, article)
                return e.config["location"]
        return None

    def _redirect_to_article(self):
        if self.urlpath:
            return redirect("wiki:get", path=self.urlpath.path)
        return redirect("wiki:get", article_id=self.article.id)

    @method_decorator(get_article(can_write=True, not_locked=True))
    def dispatch(self, request, article, *args, **kwargs):
        self.location = kwargs.pop("location", 0)
        self.header_id = kwargs.pop("header", 0)

        self.urlpath = kwargs.get("urlpath")
        kwargs["path"] = self.urlpath.path

        if request.method == "GET":
            text = article.current_revision.content
            location = self.locate_section(article, text)
            if location:
                self.orig_section = text[location[0] : location[1]]
                # Pass the to be used content to EditSection
                kwargs["content"] = self.orig_section
                request.session["editsection_content"] = self.orig_section
            else:
                messages.error(
                    request, " ".format(ERROR_SECTION_CHANGED, ERROR_TRY_AGAIN)
                )
                return self._redirect_to_article()
        else:
            kwargs["content"] = request.session.get("editsection_content")
            self.orig_section = kwargs.get("content")

        return super().dispatch(request, article, *args, **kwargs)

    def form_valid(self, form):
        super().form_valid(form)

        section = self.article.current_revision.content
        if not section.endswith("\n"):
            section += "\r\n\r\n"
        text = get_object_or_404(
            models.ArticleRevision,
            article=self.article,
            id=self.article.current_revision.previous_revision.id,
        ).content

        location = self.locate_section(self.article, text)
        if location:
            if self.orig_section != text[location[0] : location[1]]:
                messages.warning(
                    self.request,
                    " ".format(
                        ERROR_SECTION_CHANGED, ERROR_SECTION_UNSAVED, ERROR_TRY_AGAIN
                    ),
                )
            # Include the edited section into the complete previous article
            self.article.current_revision.content = (
                text[0 : location[0]] + section + text[location[1] :]
            )
            self.article.current_revision.save()
        else:
            # Back to the version before replacing the article with the section
            self.article.current_revision = (
                self.article.current_revision.previous_revision
            )
            self.article.save()
            messages.error(
                self.request, " ".format(ERROR_ARTICLE_CHANGED, ERROR_TRY_AGAIN)
            )

        return self._redirect_to_article()
