import re

from markdown.extensions.toc import TocTreeprocessor, TocExtension, slugify
from markdown.util import etree
from wiki.plugins.macros import settings

HEADER_ID_PREFIX = "wiki-toc-"

IDCOUNT_RE = re.compile(r'^(.*)_([0-9]+)$')


def wiki_slugify(*args, **kwargs):
    return HEADER_ID_PREFIX + slugify(*args, **kwargs)


class WikiTreeProcessorClass(TocTreeprocessor):

    def build_toc_etree(self, div, toc_list):
        # Add title to the div
        if self.config["title"]:
            header = etree.SubElement(div, "span")
            header.attrib["class"] = "toctitle"
            header.text = self.config["title"]

        def build_etree_ul(toc_list, parent):
            ul = etree.SubElement(parent, "ul")
            for item in toc_list:
                # List item link, to be inserted into the toc div
                li = etree.SubElement(ul, "li")
                link = etree.SubElement(li, "a")
                link.text = item.get('name', '')
                link.attrib["href"] = '#' + item.get('id', '')
                if item['children']:
                    build_etree_ul(item['children'], li)
            return ul

        return build_etree_ul(toc_list, div)


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
