from unittest.mock import patch

import markdown
from django.test import TestCase
from wiki.core.markdown import ArticleMarkdown
from wiki.core.markdown.mdx.codehilite import WikiCodeHiliteExtension
from wiki.core.markdown.mdx.responsivetable import ResponsiveTableExtension
from wiki.models import URLPath

from ..base import ArticleTestBase

try:
    import pygments

    pygments = True  # NOQA
except ImportError:
    pygments = False


class ArticleMarkdownTests(ArticleTestBase):
    @patch("wiki.core.markdown.settings")
    def test_do_not_modify_extensions(self, settings):
        extensions = ["footnotes", "attr_list", "sane_lists"]
        settings.MARKDOWN_KWARGS = {"extensions": extensions}
        number_of_extensions = len(extensions)
        ArticleMarkdown(None)
        self.assertEqual(len(extensions), number_of_extensions)

    def test_html_removal(self):
        urlpath = URLPath.create_urlpath(
            self.root,
            "html_removal",
            title="Test 1",
            content="</html>only_this",
        )

        self.assertEqual(urlpath.article.render(), "<p>only_this</p>")


class ResponsiveTableExtensionTests(TestCase):
    def setUp(self):
        super().setUp()
        self.md = markdown.Markdown(
            extensions=["extra", ResponsiveTableExtension()]
        )
        self.md_without = markdown.Markdown(extensions=["extra"])

    def test_wrapping(self):
        text = "|th|th|\n|--|--|\n|td|td|"
        expected = (
            '<div class="table-responsive">\n'
            + self.md_without.convert(text)
            + "\n</div>"
        )
        self.assertEqual(self.md.convert(text), expected)


class CodehiliteTests(TestCase):
    def test_fenced_code(self):
        md = markdown.Markdown(extensions=["extra", WikiCodeHiliteExtension()])
        text = (
            "Code:\n"
            "\n"
            "```python\n"
            "echo 'line 1'\n"
            "echo 'line 2'\n"
            "```\n"
        )
        result = (
            (
                """<p>Code:</p>\n"""
                """<div class="codehilite-wrap"><div class="codehilite"><pre><span></span><code><span class="n">echo</span> <span class="s1">&#39;line 1&#39;</span>\n"""
                """<span class="n">echo</span> <span class="s1">&#39;line 2&#39;</span>\n"""
                """</code></pre></div>\n"""
                """</div>"""
            )
            if pygments
            else (
                """<p>Code:</p>\n"""
                """<div class="codehilite-wrap"><pre class="codehilite"><code class="language-python">echo 'line 1'\n"""
                """echo 'line 2'\n</code></pre>\n"""
                """</div>"""
            )
        )
        self.assertEqual(
            md.convert(text),
            result,
        )

    def test_indented_code(self):
        md = markdown.Markdown(extensions=["extra", WikiCodeHiliteExtension()])
        text = (
            "Code:\n"
            "\n"
            "    #!/usr/bin/python\n"
            "    print('line 1')\n"
            "    print('line 2')\n"
            "    print('æøå')\n"
            "\n"
        )
        result = (
            (
                """<p>Code:</p>\n"""
                """<div class="codehilite-wrap"><div class="codehilite"><table class="codehilitetable"><tr><td class="linenos"><div class="linenodiv"><pre><span class="normal">1</span>\n"""
                """<span class="normal">2</span>\n"""
                """<span class="normal">3</span>\n"""
                """<span class="normal">4</span></pre></div></td><td class="code"><div><pre><span></span><code><span class="ch">#!/usr/bin/python</span>\n"""
                """<span class="nb">print</span><span class="p">(</span><span class="s1">&#39;line 1&#39;</span><span class="p">)</span>\n"""
                """<span class="nb">print</span><span class="p">(</span><span class="s1">&#39;line 2&#39;</span><span class="p">)</span>\n"""
                """<span class="nb">print</span><span class="p">(</span><span class="s1">&#39;æøå&#39;</span><span class="p">)</span>\n"""
                """</code></pre></div></td></tr></table></div>\n"""
                """</div>"""
            )
            if pygments
            else (
                """<p>Code:</p>\n"""
                """<div class="codehilite-wrap"><pre class="codehilite"><code class="language-python linenums">#!/usr/bin/python\n"""
                """print('line 1')\n"""
                """print('line 2')\n"""
                """print('æøå')\n</code></pre>\n"""
                """</div>"""
            )
        )
        self.assertEqual(
            md.convert(text),
            result,
        )
