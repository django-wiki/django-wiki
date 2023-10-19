from django.test import TestCase
from markdown import Markdown
from wiki.core import markdown
from wiki.plugins.macros.mdx.toc import WikiTocExtension

from tests.base import RequireRootArticleMixin
from tests.base import TestBase


class TocMacroTests(TestCase):
    def test_toc_renders_table_of_content(self):
        """Verifies that the [TOC] wiki code renders a Table of Content"""
        md = Markdown(extensions=["extra", WikiTocExtension()])
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
            "<ul>\n"
            '<li><a href="#wiki-toc-first-title">First title.</a><ul>\n'
            '<li><a href="#wiki-toc-subsection">Subsection</a></li>\n'
            "</ul>\n"
            "</li>\n"
            "</ul>\n"
            "</div>\n"
            '<h1 id="wiki-toc-first-title">First title.</h1>\n'
            "<p>Paragraph 1</p>\n"
            '<h2 id="wiki-toc-subsection">Subsection</h2>\n'
            "<p>Paragraph 2</p>"
        )
        self.assertEqual(md.convert(text), expected_output)

    def test_toc_renders_table_of_content_with_kwargs(self):
        """Verifies that the [TOC] wiki code renders a Table of Content"""
        md = Markdown(extensions=["extra", WikiTocExtension(title="test")])
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
            '<div class="toc"><span class="toctitle">test</span><ul>\n'
            '<li><a href="#wiki-toc-first-title">First title.</a><ul>\n'
            '<li><a href="#wiki-toc-subsection">Subsection</a></li>\n'
            "</ul>\n"
            "</li>\n"
            "</ul>\n"
            "</div>\n"
            '<h1 id="wiki-toc-first-title">First title.</h1>\n'
            "<p>Paragraph 1</p>\n"
            '<h2 id="wiki-toc-subsection">Subsection</h2>\n'
            "<p>Paragraph 2</p>"
        )
        self.assertEqual(md.convert(text), expected_output)


class TocMacroTestsInWiki(RequireRootArticleMixin, TestBase):
    def test_toc_renders_table_of_content_in_wiki(self):
        md = markdown.ArticleMarkdown(article=self.root_article)
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
            '<div class="toc"><span class="toctitle">Contents</span><ul>\n'
            '<li><a href="#wiki-toc-first-title">First title.</a><ul>\n'
            '<li><a href="#wiki-toc-subsection">Subsection</a></li>\n'
            "</ul>\n"
            "</li>\n"
            "</ul>\n"
            "</div>\n"
            '<h1 id="wiki-toc-first-title">First title.<a class="article-edit-title-link" '
            'href="/_plugin/editsection/header/wiki-toc-first-title/">[edit]</a></h1>\n'
            "<p>Paragraph 1</p>\n"
            '<h2 id="wiki-toc-subsection">Subsection<a class="article-edit-title-link" '
            'href="/_plugin/editsection/header/wiki-toc-subsection/">[edit]</a></h2>\n'
            "<p>Paragraph 2</p>"
        )
        self.assertEqual(md.convert(text), expected_output)

    def test_toc_renders_table_of_content_with_toc_class(self):
        md = markdown.ArticleMarkdown(article=self.root_article)
        text = (
            "[TOC toc_class:'nontoc test']\n"
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
            '<div class="nontoc test"><span class="toctitle">Contents</span><ul>\n'
            '<li><a href="#wiki-toc-first-title">First title.</a><ul>\n'
            '<li><a href="#wiki-toc-subsection">Subsection</a></li>\n'
            "</ul>\n"
            "</li>\n"
            "</ul>\n"
            "</div>\n"
            '<h1 id="wiki-toc-first-title">First title.<a class="article-edit-title-link" '
            'href="/_plugin/editsection/header/wiki-toc-first-title/">[edit]</a></h1>\n'
            "<p>Paragraph 1</p>\n"
            '<h2 id="wiki-toc-subsection">Subsection<a class="article-edit-title-link" '
            'href="/_plugin/editsection/header/wiki-toc-subsection/">[edit]</a></h2>\n'
            "<p>Paragraph 2</p>"
        )
        self.assertEqual(md.convert(text), expected_output)

    def test_toc_renders_table_of_content_in_wiki_with_kwargs(self):
        md = markdown.ArticleMarkdown(article=self.root_article)
        text = (
            "[TOC title:test]\n"
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
            '<div class="toc"><span class="toctitle">test</span><ul>\n'
            '<li><a href="#wiki-toc-first-title">First title.</a><ul>\n'
            '<li><a href="#wiki-toc-subsection">Subsection</a></li>\n'
            "</ul>\n"
            "</li>\n"
            "</ul>\n"
            "</div>\n"
            '<h1 id="wiki-toc-first-title">First title.<a class="article-edit-title-link" '
            'href="/_plugin/editsection/header/wiki-toc-first-title/">[edit]</a></h1>\n'
            "<p>Paragraph 1</p>\n"
            '<h2 id="wiki-toc-subsection">Subsection<a class="article-edit-title-link" '
            'href="/_plugin/editsection/header/wiki-toc-subsection/">[edit]</a></h2>\n'
            "<p>Paragraph 2</p>"
        )
        self.assertEqual(md.convert(text), expected_output)

    def test_toc_renders_table_of_content_in_wiki_with_depth(self):
        md = markdown.ArticleMarkdown(article=self.root_article)
        text = (
            "[TOC toc_depth:1]\n"
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
            '<div class="toc"><span class="toctitle">Contents</span><ul>\n'
            '<li><a href="#wiki-toc-first-title">First title.</a></li>\n'
            "</ul>\n"
            "</div>\n"
            '<h1 id="wiki-toc-first-title">First title.<a class="article-edit-title-link" '
            'href="/_plugin/editsection/header/wiki-toc-first-title/">[edit]</a></h1>\n'
            "<p>Paragraph 1</p>\n"
            '<h2 id="wiki-toc-subsection">Subsection<a class="article-edit-title-link" '
            'href="/_plugin/editsection/header/wiki-toc-subsection/">[edit]</a></h2>\n'
            "<p>Paragraph 2</p>"
        )
        self.assertEqual(md.convert(text), expected_output)

    def test_toc_renders_table_of_content_in_wiki_with_multi_kwargs(self):
        md = markdown.ArticleMarkdown(article=self.root_article)
        text = (
            "[TOC title:'test' toc_depth:'1' anchorlink:'True']\n"
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
            '<div class="toc"><span class="toctitle">test</span><ul>\n'
            '<li><a href="#wiki-toc-first-title">First title.</a></li>\n'
            "</ul>\n"
            "</div>\n"
            '<h1 id="wiki-toc-first-title"><a class="toclink" '
            'href="#wiki-toc-first-title">First title.</a><a '
            'class="article-edit-title-link" '
            'href="/_plugin/editsection/header/wiki-toc-first-title/">[edit]</a></h1>\n'
            "<p>Paragraph 1</p>\n"
            '<h2 id="wiki-toc-subsection"><a class="toclink" '
            'href="#wiki-toc-subsection">Subsection</a><a class="article-edit-title-link" '
            'href="/_plugin/editsection/header/wiki-toc-subsection/">[edit]</a></h2>\n'
            "<p>Paragraph 2</p>"
        )
        self.assertEqual(md.convert(text), expected_output)

    def test_toc_renders_table_of_content_in_wiki_wrong_type(self):
        md = markdown.ArticleMarkdown(article=self.root_article)
        text = (
            "[TOC anchorlink:Yes]\n"
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
            '<div class="toc"><span class="toctitle">Contents</span><ul>\n'
            '<li><a href="#wiki-toc-first-title">First title.</a><ul>\n'
            '<li><a href="#wiki-toc-subsection">Subsection</a></li>\n'
            "</ul>\n"
            "</li>\n"
            "</ul>\n"
            "</div>\n"
            '<h1 id="wiki-toc-first-title">First title.<a class="article-edit-title-link" '
            'href="/_plugin/editsection/header/wiki-toc-first-title/">[edit]</a></h1>\n'
            "<p>Paragraph 1</p>\n"
            '<h2 id="wiki-toc-subsection">Subsection<a class="article-edit-title-link" '
            'href="/_plugin/editsection/header/wiki-toc-subsection/">[edit]</a></h2>\n'
            "<p>Paragraph 2</p>"
        )
        self.assertEqual(md.convert(text), expected_output)

    def test_toc_renders_table_of_content_in_wiki_test_bool_one(self):
        # Test if the integer is 1 and should be True
        md = markdown.ArticleMarkdown(article=self.root_article)
        text = (
            "[TOC anchorlink:1]\n"
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
            '<div class="toc"><span class="toctitle">Contents</span><ul>\n'
            '<li><a href="#wiki-toc-first-title">First title.</a><ul>\n'
            '<li><a href="#wiki-toc-subsection">Subsection</a></li>\n'
            "</ul>\n"
            "</li>\n"
            "</ul>\n"
            "</div>\n"
            '<h1 id="wiki-toc-first-title"><a class="toclink" '
            'href="#wiki-toc-first-title">First title.</a><a '
            'class="article-edit-title-link" '
            'href="/_plugin/editsection/header/wiki-toc-first-title/">[edit]</a></h1>\n'
            "<p>Paragraph 1</p>\n"
            '<h2 id="wiki-toc-subsection"><a class="toclink" '
            'href="#wiki-toc-subsection">Subsection</a><a class="article-edit-title-link" '
            'href="/_plugin/editsection/header/wiki-toc-subsection/">[edit]</a></h2>\n'
            "<p>Paragraph 2</p>"
        )
        self.assertEqual(md.convert(text), expected_output)

    def test_toc_renders_table_of_content_in_wiki_test_bool_zero(self):
        # Test if the integer is zero and should be false
        md = markdown.ArticleMarkdown(article=self.root_article)
        text = (
            "[TOC anchorlink:0]\n"
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
            '<div class="toc"><span class="toctitle">Contents</span><ul>\n'
            '<li><a href="#wiki-toc-first-title">First title.</a><ul>\n'
            '<li><a href="#wiki-toc-subsection">Subsection</a></li>\n'
            "</ul>\n"
            "</li>\n"
            "</ul>\n"
            "</div>\n"
            '<h1 id="wiki-toc-first-title">First title.<a class="article-edit-title-link" '
            'href="/_plugin/editsection/header/wiki-toc-first-title/">[edit]</a></h1>\n'
            "<p>Paragraph 1</p>\n"
            '<h2 id="wiki-toc-subsection">Subsection<a class="article-edit-title-link" '
            'href="/_plugin/editsection/header/wiki-toc-subsection/">[edit]</a></h2>\n'
            "<p>Paragraph 2</p>"
        )
        self.assertEqual(md.convert(text), expected_output)

    def test_toc_renders_table_of_content_in_wiki_test_bool_wrong(self):
        # Test if the integer is wrong value
        md = markdown.ArticleMarkdown(article=self.root_article)
        text = (
            "[TOC anchorlink:5]\n"
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
            '<div class="toc"><span class="toctitle">Contents</span><ul>\n'
            '<li><a href="#wiki-toc-first-title">First title.</a><ul>\n'
            '<li><a href="#wiki-toc-subsection">Subsection</a></li>\n'
            "</ul>\n"
            "</li>\n"
            "</ul>\n"
            "</div>\n"
            '<h1 id="wiki-toc-first-title">First title.<a class="article-edit-title-link" '
            'href="/_plugin/editsection/header/wiki-toc-first-title/">[edit]</a></h1>\n'
            "<p>Paragraph 1</p>\n"
            '<h2 id="wiki-toc-subsection">Subsection<a class="article-edit-title-link" '
            'href="/_plugin/editsection/header/wiki-toc-subsection/">[edit]</a></h2>\n'
            "<p>Paragraph 2</p>"
        )
        self.assertEqual(md.convert(text), expected_output)
