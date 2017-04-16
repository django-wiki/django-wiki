from __future__ import absolute_import, unicode_literals

from mock import patch
from wiki.core.markdown import ArticleMarkdown
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
