import markdown
from django.test import TestCase
from wiki.plugins.macros.mdx.toc import WikiTocExtension


class TocMacroTests(TestCase):
    def test_toc_renders_table_of_content(self):
        """ Verifies that the [TOC] wiki code renders a Table of Content
        """
        md = markdown.Markdown(
            extensions=['extra', WikiTocExtension()]
        )
        text = (
            "[TOC]\n"
            "\n"
            "# First title.\n"
            "\n"
            "Paragraph 1\n"
            "\n"
            "## Subsection\n"
            "\n"
            "Paragraph 2"
        )
        expected_output = (
            '<div class="toc">\n'
            '<ul>\n'
            '<li><a href="#wiki-toc-first-title">First title.</a><ul>\n'
            '<li><a href="#wiki-toc-subsection">Subsection</a></li>\n'
            '</ul>\n'
            '</li>\n'
            '</ul>\n'
            '</div>\n'
            '<h1 id="wiki-toc-first-title">First title.</h1>\n'
            '<p>Paragraph 1</p>\n'
            '<h2 id="wiki-toc-subsection">Subsection</h2>\n'
            '<p>Paragraph 2</p>'
        )
        self.assertEqual(md.convert(text), expected_output)
