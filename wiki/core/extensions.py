from markdown.extensions import Extension

from .processors import AnchorTagProcessor


class AnchorTagExtension(Extension):
    """
    Custom extension to register anchor tag processor with Markdown.
    """

    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add('AnchorTagProcessor', AnchorTagProcessor(md), '>inline')
