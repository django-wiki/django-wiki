import re

from markdown.extensions.toc import TocExtension, TocTreeprocessor, slugify
from wiki.plugins.macros import settings

HEADER_ID_PREFIX = "wiki-toc-"

IDCOUNT_RE = re.compile(r'^(.*)_([0-9]+)$')


def wiki_slugify(*args, **kwargs):
    return HEADER_ID_PREFIX + slugify(*args, **kwargs)


class WikiTreeProcessorClass(TocTreeprocessor):

    def run(self, doc):
        # Necessary because self.title is set to a LazyObject via gettext_lazy
        if self.title:
            self.title = str(self.title)
        super().run(doc)


class WikiTocExtension(TocExtension):
    TreeProcessorClass = WikiTreeProcessorClass

    def __init__(self, **kwargs):
        kwargs.setdefault('slugify', wiki_slugify)
        super().__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        if 'toc' in settings.METHODS:
            TocExtension.extendMarkdown(self, md, md_globals)


def makeExtension(*args, **kwargs):
    """Return an instance of the extension."""
    return WikiTocExtension(*args, **kwargs)
