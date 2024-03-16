from textwrap import dedent

import logging
import re

from markdown.extensions.codehilite import CodeHilite
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.preprocessors import Preprocessor
from markdown.treeprocessors import Treeprocessor
from wiki.core.markdown import add_to_registry


logger = logging.getLogger(__name__)


def highlight(code, config, tab_length, lang=None):
    code = CodeHilite(
        code,
        linenums=config["linenums"],
        guess_lang=config["guess_lang"],
        css_class=config["css_class"],
        style=config["pygments_style"],
        noclasses=config["noclasses"],
        tab_length=tab_length,
        use_pygments=config["use_pygments"],
        lang=lang,
    )
    html = code.hilite()
    html = f"""<div class="codehilite-wrap">{html}</div>"""
    return html


class WikiFencedBlockPreprocessor(Preprocessor):
    """
    This is a replacement of markdown.extensions.fenced_code which will
    directly and without configuration options invoke the vanilla CodeHilite
    extension.
    """

    FENCED_BLOCK_RE = re.compile(
        dedent(
            r"""
            (?P<fence>^(?:~{3,}|`{3,}))[ ]*                          # opening fence
            ((\{(?P<attrs>[^\}\n]*)\})|                              # (optional {attrs} or
            (\.?(?P<lang>[\w#.+-]*)[ ]*)?                            # optional (.)lang
            (hl_lines=(?P<quot>"|')(?P<hl_lines>.*?)(?P=quot)[ ]*)?) # optional hl_lines)
            \n                                                       # newline (end of opening fence)
            (?P<code>.*?)(?<=\n)                                     # the code block
            (?P=fence)[ ]*$                                          # closing fence
        """
        ),
        re.MULTILINE | re.DOTALL | re.VERBOSE,
    )
    CODE_WRAP = "<pre>%s</pre>"

    def __init__(self, md):
        super().__init__(md)

        self.checked_for_codehilite = False
        self.codehilite_conf = {}

    def run(self, lines):
        """Match and store Fenced Code Blocks in the HtmlStash."""

        text = "\n".join(lines)
        while 1:
            m = self.FENCED_BLOCK_RE.search(text)
            if m:
                lang = ""
                if m.group("lang"):
                    lang = m.group("lang")
                html = highlight(
                    m.group("code"), self.config, self.md.tab_length, lang=lang
                )
                placeholder = self.md.htmlStash.store(html)
                text = "{}\n{}\n{}".format(
                    text[: m.start()],
                    placeholder,
                    text[m.end() :],
                )
            else:
                break
        return text.split("\n")


class HiliteTreeprocessor(Treeprocessor):
    """Hilight source code in code blocks."""

    def code_unescape(self, text):
        """Unescape &, <, > and " characters."""
        text = text.replace("&amp;", "&")
        text = text.replace("&lt;", "<")
        text = text.replace("&gt;", ">")
        text = text.replace("&quot;", '"')
        return text

    def run(self, root):
        """Find code blocks and store in htmlStash."""
        blocks = root.iter("pre")
        for block in blocks:
            if len(block) == 1 and block[0].tag == "code":
                html = highlight(
                    self.code_unescape(block[0].text),
                    self.config,
                    self.md.tab_length,
                )
                placeholder = self.md.htmlStash.store(html)
                # Clear codeblock in etree instance
                block.clear()
                # Change to p element which will later
                # be removed when inserting raw html
                block.tag = "p"
                block.text = placeholder


class WikiCodeHiliteExtension(CodeHiliteExtension):
    """
    markdown.extensions.codehilite cannot configure container tags but forces
    code to be in <table></table>, so we had to overwrite some of the code
    because it's hard to extend...
    """

    def extendMarkdown(self, md):
        """Add HilitePostprocessor to Markdown instance."""
        hiliter = HiliteTreeprocessor(md)
        hiliter.config = self.getConfigs()
        if "hilite" in md.treeprocessors:
            logger.warning(
                "Replacing existing 'hilite' extension - please remove "
                "'codehilite' from WIKI_MARKDOWN_KWARGS"
            )
            # del md.treeprocessors["hilite"]
            md.treeprocessors.deregister("hilite")

        add_to_registry(md.treeprocessors, "hilite", hiliter, "<inline")

        if "fenced_code_block" in md.preprocessors:
            logger.warning(
                "Replacing existing 'fenced_code_block' extension - please remove "
                "'fenced_code_block' or 'extras' from WIKI_MARKDOWN_KWARGS"
            )
            # del md.preprocessors["fenced_code_block"]
            md.preprocessors.deregister("fenced_code_block")
        hiliter = WikiFencedBlockPreprocessor(md)
        hiliter.config = self.getConfigs()

        add_to_registry(
            md.preprocessors,
            "fenced_code_block",
            hiliter,
            ">normalize_whitespace",
        )

        md.registerExtension(self)


def makeExtension(*args, **kwargs):
    """Return an instance of the extension."""
    return WikiCodeHiliteExtension(*args, **kwargs)
