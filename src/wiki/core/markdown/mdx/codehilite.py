from __future__ import unicode_literals

import logging
import re

from markdown.extensions.codehilite import CodeHilite, CodeHiliteExtension
from markdown.preprocessors import Preprocessor
from markdown.treeprocessors import Treeprocessor

logger = logging.getLogger(__name__)


def highlight(code, config, tab_length, lang=None):
    code = CodeHilite(
        code,
        linenums=config['linenums'],
        guess_lang=config['guess_lang'],
        css_class=config['css_class'],
        style=config['pygments_style'],
        noclasses=config['noclasses'],
        tab_length=tab_length,
        use_pygments=config['use_pygments'],
        lang=lang,
    )
    html = code.hilite()
    html = """<div class="codehilite-wrap">{}</div>""".format(html)
    return html


class WikiFencedBlockPreprocessor(Preprocessor):
    """
    This is a replacement of markdown.extensions.fenced_code which will
    directly and without configuration options invoke the vanilla CodeHilite
    extension.
    """
    FENCED_BLOCK_RE = re.compile(r'''
(?P<fence>^(?:~{3,}|`{3,}))[ ]*         # Opening ``` or ~~~
(\{?\.?(?P<lang>[a-zA-Z0-9_+-]*))?[ ]*  # Optional {, and lang
# Optional highlight lines, single- or double-quote-delimited
(hl_lines=(?P<quot>"|')(?P<hl_lines>.*?)(?P=quot))?[ ]*
}?[ ]*\n                                # Optional closing }
(?P<code>.*?)(?<=\n)
(?P=fence)[ ]*$''', re.MULTILINE | re.DOTALL | re.VERBOSE)
    CODE_WRAP = '<pre>%s</pre>'

    def __init__(self, md):
        super(WikiFencedBlockPreprocessor, self).__init__(md)

        self.checked_for_codehilite = False
        self.codehilite_conf = {}

    def run(self, lines):
        """ Match and store Fenced Code Blocks in the HtmlStash. """

        text = "\n".join(lines)
        while 1:
            m = self.FENCED_BLOCK_RE.search(text)
            if m:
                lang = ''
                if m.group('lang'):
                    lang = m.group('lang')
                html = highlight(m.group('code'), self.config, self.markdown.tab_length, lang=lang)
                placeholder = self.markdown.htmlStash.store(html, safe=True)
                text = '%s\n%s\n%s' % (text[:m.start()],
                                       placeholder,
                                       text[m.end():])
            else:
                break
        return text.split("\n")


class HiliteTreeprocessor(Treeprocessor):
    """ Hilight source code in code blocks. """

    def run(self, root):
        """ Find code blocks and store in htmlStash. """
        blocks = root.iter('pre')
        for block in blocks:
            if len(block) == 1 and block[0].tag == 'code':
                html = highlight(block[0].text, self.config, self.markdown.tab_length)
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

        if "fenced_code_block" in md.preprocessors:
            logger.warning(
                "Replacing existing 'fenced_code_block' extension - please remove "
                "'fenced_code_block' or 'extras' from WIKI_MARKDOWN_KWARGS"
            )
            del md.preprocessors["fenced_code_block"]
        hiliter = WikiFencedBlockPreprocessor(md)
        hiliter.config = self.getConfigs()
        md.preprocessors.add('fenced_code_block',
                             hiliter,
                             ">normalize_whitespace")

        md.registerExtension(self)
