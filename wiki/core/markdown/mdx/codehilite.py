import logging

from markdown.extensions.codehilite import CodeHilite, CodeHiliteExtension
from markdown.treeprocessors import Treeprocessor

logger = logging.getLogger(__name__)


class HiliteTreeprocessor(Treeprocessor):
    """ Hilight source code in code blocks. """

    def run(self, root):
        """ Find code blocks and store in htmlStash. """
        blocks = root.iter('pre')
        for block in blocks:
            if len(block) == 1 and block[0].tag == 'code':
                code = CodeHilite(
                    block[0].text,
                    linenums=self.config['linenums'],
                    guess_lang=self.config['guess_lang'],
                    css_class=self.config['css_class'],
                    style=self.config['pygments_style'],
                    noclasses=self.config['noclasses'],
                    tab_length=self.markdown.tab_length,
                    use_pygments=self.config['use_pygments']
                )
                html = code.hilite()
                html = """<div class="codehilite-wrap">{}</div>""".format(html)
                placeholder = self.markdown.htmlStash.store(html, safe=True)
                # Clear codeblock in etree instance
                block.clear()
                # Change to p element which will later
                # be removed when inserting raw html
                block.tag = 'p'
                block.text = placeholder


class WikiCodeHiliteExtension(CodeHiliteExtension):
    """
    markdown.extensions.codehilite cannot configure container tags but forces
    code to be in <table></table>, so we had to overwrite some of the code
    because it's hard to extend...
    """

    def extendMarkdown(self, md, md_globals):
        """ Add HilitePostprocessor to Markdown instance. """
        hiliter = HiliteTreeprocessor(md)
        hiliter.config = self.getConfigs()
        if "hilite" in md.treeprocessors:
            logger.warning(
                "Replacing existing 'hilite' extension - please remove "
                "'codehilite' from WIKI_MARKDOWN_KWARGS"
            )
            del md.treeprocessors["hilite"]
        md.treeprocessors.add("hilite", hiliter, "<inline")

        md.registerExtension(self)
