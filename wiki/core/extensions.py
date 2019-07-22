from __future__ import absolute_import

from markdown.extensions import Extension

from wiki.core.processors import AnchorTagProcessor


class AnchorTagExtension(Extension):
    """
    Custom extension to register anchor tag processor with Markdown.
    """
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add('AnchorTagProcessor', AnchorTagProcessor(md), '>inline')
