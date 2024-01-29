from django.test import TestCase
from markdown import Markdown
from wiki.core import markdown
from wiki.plugins.pymdown import wiki_plugin

from tests.base import RequireRootArticleMixin
from tests.base import TestBase


class TocMacroTests(TestCase):
    """
    This is used to test the PyMdown extensions module independently of Django Wiki. If this fails
    it should because something has changed on with PyMdown or Markdown itself.
    """

    def test_pymdown_renders_block_details(self):
        extensions = ["extra"]
        extensions.extend(wiki_plugin.PymdownPlugin.markdown_extensions)
        md = Markdown(extensions=extensions)
        text = "/// details | Some summary\n" "\n" "Some content\b" "///\n"
        expected_output = (
            "<details>\n"
            "<summary>Some summary</summary>\n"
            "<p>Some content\x08///</p>\n"
            "</details>"
        )
        self.assertEqual(expected_output, md.convert(text))

    def test_pymdown_renders_block_details_with_type(self):
        extensions = ["extra"]
        extensions.extend(wiki_plugin.PymdownPlugin.markdown_extensions)
        md = Markdown(extensions=extensions)
        text = (
            "/// details | Some summary\n"
            "    type: warning\n"
            "\n"
            "Some content\b"
            "///\n"
        )
        expected_output = (
            '<details class="warning">\n'
            "<summary>Some summary</summary>\n"
            "<p>Some content\x08///</p>\n"
            "</details>"
        )
        self.assertEqual(expected_output, md.convert(text))

    def test_pymdown_renders_block_admonition(self):
        extensions = ["extra"]
        extensions.extend(wiki_plugin.PymdownPlugin.markdown_extensions)
        md = Markdown(extensions=extensions)
        text = "/// admonition | Some summary\n" "Some content\b" "///\n"
        expected_output = (
            '<div class="admonition">\n'
            '<p class="admonition-title">Some summary</p>\n'
            "<p>Some content\x08///</p>\n"
            "</div>"
        )
        self.assertEqual(expected_output, md.convert(text))

    def test_pymdown_renders_block_admonition_with_type(self):
        extensions = ["extra"]
        extensions.extend(wiki_plugin.PymdownPlugin.markdown_extensions)
        md = Markdown(extensions=extensions)
        text = (
            "/// admonition | Some summary\n"
            "    type: warning\n"
            "Some content\b"
            "///\n"
        )
        expected_output = (
            '<div class="admonition warning">\n'
            '<p class="admonition-title">Some summary</p>\n'
            "<p>Some content\x08///</p>\n"
            "</div>"
        )
        self.assertEqual(expected_output, md.convert(text))

    def test_pymdown_renders_block_definition(self):
        extensions = ["extra"]
        extensions.extend(wiki_plugin.PymdownPlugin.markdown_extensions)
        md = Markdown(extensions=extensions)
        text = (
            "/// define\n"
            "Apple\n"
            "\n"
            "- Pomaceous fruit of plants of the genus Malu in the family Rosaceae.\n"
            "///\n"
        )
        expected_output = (
            "<dl>\n"
            "<dt>Apple</dt>\n"
            "<dd>Pomaceous fruit of plants of the genus Malu in the family "
            "Rosaceae.</dd>\n"
            "</dl>"
        )
        self.assertEqual(expected_output, md.convert(text))

    def test_pymdown_renders_block_definition_multiples(self):
        extensions = ["extra"]
        extensions.extend(wiki_plugin.PymdownPlugin.markdown_extensions)
        md = Markdown(extensions=extensions)
        text = (
            "/// define\n"
            "Apple\n"
            "\n"
            "- Pomaceous fruit of plants of the genus Malu in the family Rosaceae.\n"
            "\n"
            "Orange\n"
            "\n"
            "- The fruit of an evergreen tree of hte genus Citrus.\n"
            "///\n"
        )
        expected_output = (
            "<dl>\n"
            "<dt>Apple</dt>\n"
            "<dd>Pomaceous fruit of plants of the genus Malu in the family "
            "Rosaceae.</dd>\n"
            "<dt>Orange</dt>\n"
            "<dd>The fruit of an evergreen tree of hte genus Citrus.</dd>\n"
            "</dl>"
        )
        self.assertEqual(expected_output, md.convert(text))

    def test_pymdown_renders_block_definition_multiple_terms(self):
        extensions = ["extra"]
        extensions.extend(wiki_plugin.PymdownPlugin.markdown_extensions)
        md = Markdown(extensions=extensions)
        text = (
            "/// define\n"
            "Term 1\n"
            "\n"
            "Term 2\n"
            "- Definition a\n"
            "\n"
            "Term 3\n"
            "\n"
            "- Definition b\n"
            "///\n"
        )
        expected_output = (
            "<dl>\n"
            "<dt>Term 1</dt>\n"
            "<dt>Term 2\n"
            "- Definition a</dt>\n"
            "<dt>Term 3</dt>\n"
            "<dd>Definition b</dd>\n"
            "</dl>"
        )
        self.assertEqual(expected_output, md.convert(text))

    def test_pymdown_renders_block_html_wrap(self):
        extensions = ["extra"]
        extensions.extend(wiki_plugin.PymdownPlugin.markdown_extensions)
        md = Markdown(extensions=extensions)
        text = (
            "/// html | div[stype='border: 1px solid red;']\n"
            "some *markdown* content\n"
            "///\n"
        )
        expected_output = (
            '<div stype="border: 1px solid red;">\n'
            "<p>some <em>markdown</em> content</p>\n"
            "</div>"
        )
        self.assertEqual(expected_output, md.convert(text))


class TocMacroTestsInWiki(RequireRootArticleMixin, TestBase):
    def test_pymdown_in_wiki_renders_block_details(self):
        wiki_plugin.settings.update_whitelist()  # Fixes testing bug
        md = markdown.ArticleMarkdown(
            article=self.root_article,
            extensions=wiki_plugin.PymdownPlugin.markdown_extensions,
        )
        text = "/// details | Some summary\n" "\n" "Some content\n" "///\n"
        expected_output = (
            "<details>\n"
            "<summary>Some summary</summary>\n"
            "<p>Some content</p>\n"
            "</details>"
        )
        self.assertEqual(expected_output, md.convert(text))

    def test_pymdown_in_wiki_renders_block_details_with_type(self):
        wiki_plugin.settings.update_whitelist()  # Fixes testing bug
        md = markdown.ArticleMarkdown(
            article=self.root_article,
            extensions=wiki_plugin.PymdownPlugin.markdown_extensions,
        )
        text = (
            "/// details | Some summary\n"
            "    type: warning\n"
            "Some content\n"
            "///\n"
        )
        expected_output = (
            '<details class="warning">\n'
            "<summary>Some summary</summary>\n"
            "<p>Some content</p>\n"
            "</details>"
        )
        self.assertEqual(expected_output, md.convert(text))

    def test_pymdown_in_wiki_renders_block_admonition(self):
        md = markdown.ArticleMarkdown(
            article=self.root_article,
            extensions=wiki_plugin.PymdownPlugin.markdown_extensions,
        )
        text = "/// admonition | Some summary\n" "Some content.\n" "///\n"
        expected_output = (
            '<div class="admonition">\n'
            '<p class="admonition-title">Some summary</p>\n'
            "<p>Some content.</p>\n"
            "</div>"
        )
        self.assertEqual(expected_output, md.convert(text))

    def test_pymdown_in_wiki_renders_block_admonition_with_type(self):
        md = markdown.ArticleMarkdown(
            article=self.root_article,
            extensions=wiki_plugin.PymdownPlugin.markdown_extensions,
        )
        text = (
            "/// admonition | Some summary\n"
            "    type: warning\n"
            "Some content.\n"
            "///\n"
        )
        expected_output = (
            '<div class="admonition warning">\n'
            '<p class="admonition-title">Some summary</p>\n'
            "<p>Some content.</p>\n"
            "</div>"
        )
        self.assertEqual(expected_output, md.convert(text))

    def test_pymdown_in_wiki_renders_block_definition(self):
        md = markdown.ArticleMarkdown(
            article=self.root_article,
            extensions=wiki_plugin.PymdownPlugin.markdown_extensions,
        )
        text = (
            "/// define\n"
            "Apple\n"
            "\n"
            "- Pomaceous fruit of plants of the genus Malu in the family Rosaceae.\n"
            "///\n"
        )
        expected_output = (
            "<dl>\n"
            "<dt>Apple</dt>\n"
            "<dd>Pomaceous fruit of plants of the genus Malu in the family "
            "Rosaceae.</dd>\n"
            "</dl>"
        )
        self.assertEqual(expected_output, md.convert(text))

    def test_pymdown_in_wiki_renders_block_definition_multiples(self):
        md = markdown.ArticleMarkdown(
            article=self.root_article,
            extensions=wiki_plugin.PymdownPlugin.markdown_extensions,
        )
        text = (
            "/// define\n"
            "Apple\n"
            "\n"
            "- Pomaceous fruit of plants of the genus Malu in the family Rosaceae.\n"
            "\n"
            "Orange\n"
            "\n"
            "- The fruit of an evergreen tree of hte genus Citrus.\n"
            "///\n"
        )
        expected_output = (
            "<dl>\n"
            "<dt>Apple</dt>\n"
            "<dd>Pomaceous fruit of plants of the genus Malu in the family "
            "Rosaceae.</dd>\n"
            "<dt>Orange</dt>\n"
            "<dd>The fruit of an evergreen tree of hte genus Citrus.</dd>\n"
            "</dl>"
        )
        self.assertEqual(expected_output, md.convert(text))

    def test_pymdown_in_wiki_renders_block_definition_multiple_terms(self):
        md = markdown.ArticleMarkdown(
            article=self.root_article,
            extensions=wiki_plugin.PymdownPlugin.markdown_extensions,
        )
        text = (
            "/// define\n"
            "Term 1\n"
            "\n"
            "Term 2\n"
            "- Definition a\n"
            "\n"
            "Term 3\n"
            "\n"
            "- Definition b\n"
            "///\n"
        )
        expected_output = (
            "<dl>\n"
            "<dt>Term 1</dt>\n"
            "<dt>Term 2\n"
            "- Definition a</dt>\n"
            "<dt>Term 3</dt>\n"
            "<dd>Definition b</dd>\n"
            "</dl>"
        )
        self.assertEqual(expected_output, md.convert(text))

    def test_pymdown_in_wiki_renders_block_html_wrap(self):
        md = markdown.ArticleMarkdown(
            article=self.root_article,
            extensions=wiki_plugin.PymdownPlugin.markdown_extensions,
        )
        text = "/// html | div.my-class\n" "some *markdown* content\n" "///\n"
        expected_output = '<div class="my-class">\n<p>some <em>markdown</em> content</p>\n</div>'
        self.assertEqual(expected_output, md.convert(text))

    def test_pymdown_in_wiki_renders_block_html_wrap_test_bleach(self):
        """
        The tags get bleached and thus this doesn't work.
        """
        md = markdown.ArticleMarkdown(
            article=self.root_article,
            extensions=wiki_plugin.PymdownPlugin.markdown_extensions,
        )
        text = (
            "/// html | div[stype='border: 1px solid red;']\n"
            "some *markdown* content\n"
            "///\n"
        )
        expected_output = (
            "<div>\n<p>some <em>markdown</em> content</p>\n</div>"
        )
        self.assertEqual(expected_output, md.convert(text))
