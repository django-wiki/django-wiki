from django.urls import reverse
from wiki.models import URLPath

from ...base import ArticleWebTestUtils, DjangoClientTestBase, RequireRootArticleMixin


class GlobalhistoryTests(RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase):

    def test_history(self):
        url = reverse('wiki:globalhistory')
        url0 = reverse('wiki:globalhistory', kwargs={'only_last': '0'})
        url1 = reverse('wiki:globalhistory', kwargs={'only_last': '1'})

        response = self.client.get(url)
        expected = (
            '(?s).*Root Article.*no log message.*'
        )
        self.assertRegexpMatches(response.rendered_content, expected)

        URLPath.create_urlpath(URLPath.root(), "testhistory1",
                               title="TestHistory1", content="a page",
                               user_message="Comment 1")
        response = self.client.get(url)
        expected = (
            '(?s).*TestHistory1.*Comment 1.*'
            'Root Article.*no log message.*'
        )
        self.assertRegexpMatches(response.rendered_content, expected)

        urlpath = URLPath.create_urlpath(
            URLPath.root(),
            "testhistory2",
            title="TestHistory2",
            content="a page",
            user_message="Comment 2"
        )
        expected = (
            '(?s).*TestHistory2.*Comment 2.*'
            'TestHistory1.*Comment 1.*'
            'Root Article.*no log message.*'
        )
        response = self.client.get(url)
        self.assertRegexpMatches(response.rendered_content, expected)

        response = self.client.get(url0)
        self.assertRegexpMatches(response.rendered_content, expected)

        response = self.client.get(url1)
        self.assertRegexpMatches(response.rendered_content, expected)

        response = self.client.post(
            reverse('wiki:edit', kwargs={'path': 'testhistory2/'}),
            {'content': 'a page modified',
             'current_revision': str(urlpath.article.current_revision.id),
             'preview': '0',
             'save': '1',
             'summary': 'Testing Revision',
             'title': 'TestHistory2Mod'}
        )

        expected = (
            '(?s).*TestHistory2Mod.*Testing Revision.*'
            'TestHistory2.*Comment 2.*'
            'TestHistory1.*Comment 1.*'
            'Root Article.*no log message.*'
        )
        response = self.client.get(url)
        self.assertRegexpMatches(response.rendered_content, expected)

        response = self.client.get(url0)
        self.assertRegexpMatches(response.rendered_content, expected)

        expected = (
            '(?s).*TestHistory2Mod.*Testing Revision.*'
            'TestHistory1.*Comment 1.*'
            'Root Article.*no log message.*'
        )
        response = self.client.get(url1)
        self.assertRegexpMatches(response.rendered_content, expected)
