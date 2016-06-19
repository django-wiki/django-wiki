from __future__ import absolute_import, unicode_literals

from django.test import TestCase
import markdown
from wiki.core.markdown.mdx.responsivetable import ResponsiveTableExtension

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
