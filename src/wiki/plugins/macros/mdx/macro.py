import re

import markdown
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from wiki.plugins.macros import settings

# See:
# http://stackoverflow.com/questions/430759/regex-for-managing-escaped-characters-for-items-like-string-literals
re_sq_short = r"'([^'\\]*(?:\\.[^'\\]*)*)'"

MACRO_RE = r"((?i)\[(?P<macro>\w+)(?P<kwargs>\s\w+\:.+)*\])"
KWARG_RE = re.compile(
    r"\s*(?P<arg>\w+)(:(?P<value>([^\']+|%s)))?" % re_sq_short, re.IGNORECASE
)


class MacroExtension(markdown.Extension):

    """ Macro plugin markdown extension for django-wiki. """

    def extendMarkdown(self, md):
        md.inlinePatterns.add("dw-macros", MacroPattern(MACRO_RE, md), ">link")


class MacroPattern(markdown.inlinepatterns.Pattern):

    """django-wiki macro preprocessor - parse text for various [some_macro] and
    [some_macro (kw:arg)*] references. """

    def handleMatch(self, m):
        macro = m.group("macro").strip()
        if macro not in settings.METHODS or not hasattr(self, macro):
            return m.group(2)

        kwargs = m.group("kwargs")
        if not kwargs:
            return getattr(self, macro)()
        kwargs_dict = {}
        for kwarg in KWARG_RE.finditer(kwargs):
            arg = kwarg.group("arg")
            value = kwarg.group("value")
            if value is None:
                value = True
            if isinstance(value, str):
                # If value is enclosed with ': Remove and
                # remove escape sequences
                if value.startswith("'") and len(value) > 2:
                    value = value[1:-1]
                    value = value.replace("\\\\", "¤KEEPME¤")
                    value = value.replace("\\", "")
                    value = value.replace("¤KEEPME¤", "\\")
            kwargs_dict[str(arg)] = value
        return getattr(self, macro)(**kwargs_dict)

    def article_list(self, depth="2"):
        html = render_to_string(
            "wiki/plugins/macros/article_list.html",
            context={
                "article_children": self.markdown.article.get_children(
                    article__current_revision__deleted=False
                ),
                "depth": int(depth) + 1,
            },
        )
        return self.markdown.htmlStash.store(html)

    article_list.meta = dict(
        short_description=_("Article list"),
        help_text=_("Insert a list of articles in this level."),
        example_code="[article_list depth:2]",
        args={"depth": _("Maximum depth to show levels for.")},
    )

    def toc(self):
        return "[TOC]"

    toc.meta = dict(
        short_description=_("Table of contents"),
        help_text=_("Insert a table of contents matching the headings."),
        example_code="[TOC]",
        args={},
    )

    def wikilink(self):
        return ""

    wikilink.meta = dict(
        short_description=_("WikiLinks"),
        help_text=_("Insert a link to another wiki page with a short notation."),
        example_code="[[WikiLink]]",
        args={},
    )


def makeExtension(*args, **kwargs):
    """Return an instance of the extension."""
    return MacroExtension(*args, **kwargs)
