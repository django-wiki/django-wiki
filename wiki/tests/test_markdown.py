from __future__ import absolute_import, unicode_literals

from django.test import TestCase
import markdown
from wiki.core.markdown import ArticleMarkdown
from wiki.core.markdown.mdx.responsivetable import ResponsiveTableExtension
from mock import patch

class ArticleMarkdownTests(TestCase):
    @patch('wiki.core.markdown.settings')
    def test_do_not_modify_extensions(self, settings):
        extensions = ['footnotes', 'attr_list', 'sane_lists']
        settings.MARKDOWN_KWARGS = {'extensions': extensions}
        number_of_extensions = len(extensions)
        ArticleMarkdown(None)
        self.assertEqual(len(extensions), number_of_extensions)

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
