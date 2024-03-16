import re

import markdown
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from wiki.core.markdown import add_to_registry
from wiki.plugins.macros import settings
from wiki.plugins.macros.mdx import toc

# See:
# http://stackoverflow.com/questions/430759/regex-for-managing-escaped-characters-for-items-like-string-literals
re_sq_short = r"'([^'\\]*(?:\\.[^'\\]*)*)'"


MACRO_RE = (
    r"""\[(?P<macro>\w+)(?P<kwargs>(\s+\w+\:([^\:\]\s]+|'[^']+'))+)*\]"""
)

KWARG_RE = re.compile(
    r"\s*(?P<arg>\w+)(:(?P<value>([^\']+|%s)))?" % re_sq_short, re.IGNORECASE
)


class MacroExtension(markdown.Extension):

    """Macro plugin markdown extension for django-wiki."""

    def extendMarkdown(self, md):
        add_to_registry(
            md.inlinePatterns, "dw-macros", MacroPattern(MACRO_RE, md), ">link"
        )


class MacroPattern(markdown.inlinepatterns.Pattern):

    """django-wiki macro preprocessor - parse text for various [some_macro] and
    [some_macro (kw:arg)*] references."""

    def __init__(self, pattern, md=None):
        """Override init in order to add IGNORECASE flag"""
        super().__init__(pattern, md=md)
        self.compiled_re = re.compile(
            r"^(.*?)%s(.*)$" % pattern,
            flags=re.DOTALL | re.UNICODE | re.IGNORECASE,
        )

    def handleMatch(self, m):
        macro = m.group("macro").strip().lower()
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
                "article_children": self.md.article.get_children(
                    article__current_revision__deleted=False
                ),
                "depth": int(depth) + 1,
            },
        )
        return self.md.htmlStash.store(html)

    article_list.meta = {
        "short_description": _("Article list"),
        "help_text": _("Insert a list of articles in this level."),
        "example_code": "[article_list depth:2]",
        "args": {"depth": _("Maximum depth to show levels for.")},
    }

    def toc(self, **kwargs):
        toc.WikiTreeProcessorClass.CACHED_KWARGS = kwargs
        return "[TOC]"

    toc.meta = {
        "short_description": _("Table of contents"),
        "help_text": _("Insert a table of contents matching the headings."),
        "example_code": "[TOC] or [TOC toc_depth:1]",
        "args": {
            "title": _(
                "Title to insert in the Table of Contents’ <div>. Defaults to Contents."
            ),
            "baselevel": _("Base level for headers. Defaults to 1."),
            "separator": _(
                "Word separator. Character which replaces white space in id. Defaults to “-”."
            ),
            "anchorlink": _(
                "Set to True to cause all headers to link to themselves. Default is False."
            ),
            "anchorlink_class": _(
                "CSS class(es) used for the link. Defaults to toclink."
            ),
            "permalink": _(
                "Set to True or a string to generate permanent links at the end of each header. Useful with Sphinx style sheets."
            ),
            "permalink_class": _(
                "CSS class(es) used for the link. Defaults to headerlink."
            ),
            "permalink_title": _(
                "Title attribute of the permanent link. Defaults to Permanent link."
            ),
            "toc_depth": _(
                "Define the range of section levels to include in the Table of Contents. A single integer (b) defines the bottom section "
                "level (<h1>..<hb>) only. A string consisting of two digits separated by a hyphen in between ('2-5'), define the top (t) "
                "and the bottom (b) (<ht>..<hb>). Defaults to 6 (bottom)."
            ),
        },
    }

    def wikilink(self):
        return ""

    wikilink.meta = {
        "short_description": _("WikiLinks"),
        "help_text": _(
            "Insert a link to another wiki page with a short notation."
        ),
        "example_code": "[[WikiLink]]",
        "args": {},
    }


def makeExtension(*args, **kwargs):
    """Return an instance of the extension."""
    return MacroExtension(*args, **kwargs)
