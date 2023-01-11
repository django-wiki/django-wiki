from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy
from wiki import models
from wiki.core.markdown import article_markdown
from wiki.decorators import get_article
from wiki.views.article import Edit as EditView


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


class EditSection(EditView):
    def locate_section(self, article, content):
        """
        locate the section to be edited, returning index of start and end
        """
        # render article to get the headers
        article_markdown(content, article)
        headers = getattr(article, "_found_headers", [])

        # find start
        start, end = None, None
        while len(headers):
            header = headers.pop(0)
            if header["slug"] == self.header_id:
                if content[header["position"] :].startswith(header["source"]):
                    start = header
                    break
        if start is None:
            # start section not found
            return None, None

        # we have the beginning, now find next section with same or higher level
        while len(headers):
            header = headers.pop(0)
            if header["level"] <= start["level"]:
                if content[header["position"] :].startswith(header["source"]):
                    end = header
                    break
                else:
                    # there should be a matching header, but we did not find it.
                    # better be safe.
                    return None, None
        return (
            (start["position"], end["position"])
            if end
            else (start["position"], len(content))
        )

    def _redirect_to_article(self):
        if self.urlpath:
            return redirect("wiki:get", path=self.urlpath.path)
        return redirect("wiki:get", article_id=self.article.id)

    @method_decorator(get_article(can_write=True, not_locked=True))
    def dispatch(self, request, article, *args, **kwargs):
        self.header_id = kwargs.pop("header", 0)
        self.urlpath = kwargs.get("urlpath")
        kwargs["path"] = self.urlpath.path
        content = article.current_revision.content

        if request.method == "GET":
            start, end = self.locate_section(article, content)
            if start is not None and end is not None:
                self.orig_section = content[start:end]
                kwargs["content"] = self.orig_section
                request.session["editsection_content"] = self.orig_section
            else:
                messages.error(
                    request, "{} {}".format(ERROR_SECTION_CHANGED, ERROR_TRY_AGAIN)
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
        content = get_object_or_404(
            models.ArticleRevision,
            article=self.article,
            id=self.article.current_revision.previous_revision.id,
        ).content
        start, end = self.locate_section(self.article, content)
        if start is not None and end is not None:
            # compare saved original section with last version, so we
            # can detect if someone else changed it in the meantime
            if self.orig_section != content[start:end]:
                messages.warning(
                    self.request,
                    "{} {} {}".format(
                        ERROR_SECTION_CHANGED, ERROR_SECTION_UNSAVED, ERROR_TRY_AGAIN
                    ),
                )
            # Include the edited section into the complete previous article
            self.article.current_revision.content = (
                content[0:start] + section + content[end:]
            )
            self.article.current_revision.save()
        else:
            # Back to the version before replacing the article with the section
            self.article.current_revision = (
                self.article.current_revision.previous_revision
            )
            self.article.save()
            messages.error(
                self.request, "{} {}".format(ERROR_ARTICLE_CHANGED, ERROR_TRY_AGAIN)
            )

        return self._redirect_to_article()
