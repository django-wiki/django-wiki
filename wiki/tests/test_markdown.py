from __future__ import absolute_import, unicode_literals

import markdown
from django.test import TestCase
from mock import patch
from wiki.core.markdown import ArticleMarkdown
from wiki.core.markdown.mdx.responsivetable import ResponsiveTableExtension
from wiki.models import URLPath
from wiki.tests.base import ArticleTestBase


class ArticleMarkdownTests(ArticleTestBase):

    @patch('wiki.core.markdown.settings')
    def test_do_not_modify_extensions(self, settings):
        extensions = ['footnotes', 'attr_list', 'sane_lists']
        settings.MARKDOWN_KWARGS = {'extensions': extensions}
        number_of_extensions = len(extensions)
        ArticleMarkdown(None)
        self.assertEqual(len(extensions), number_of_extensions)

    def test_html_removal(self):

        urlpath = URLPath.create_article(
            self.root,
            'html_removal',
            title="Test 1",
            content="</html>only_this"
        )

        self.assertEqual(urlpath.article.render(), "<p>&lt;/html&gt;only_this</p>")


class ResponsiveTableTests(TestCase):

    def setUp(self):
        self.md = markdown.Markdown(extensions=[
            'extra',
            ResponsiveTableExtension()
        ])
        self.md_without = markdown.Markdown(extensions=['extra'])

    def test_wrapping(self):
        text = '|th|th|\n|--|--|\n|td|td|'
        expected = '<div class="table-responsive">\n' + self.md_without.convert(text) + '\n</div>'
        self.assertEqual(self.md.convert(text), expected)
