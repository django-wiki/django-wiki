from __future__ import print_function, unicode_literals

import sys

from django.core.urlresolvers import reverse
from wiki.models import URLPath

from ...base import (ArticleWebTestUtils, DjangoClientTestBase,
                     RequireRootArticleMixin)


class GlobalhistoryTests(RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase):

    def _assertRegex(self, a, b):
        if sys.version_info >= (3, 2):
            return self.assertRegex(a, b)
        else:
            return self.assertRegexpMatches(a, b)

    def test_history(self):
        url = reverse('wiki:globalhistory')
        url0 = reverse('wiki:globalhistory', kwargs={'only_last': '0'})
        url1 = reverse('wiki:globalhistory', kwargs={'only_last': '1'})

        response = self.c.get(url)
        expected = (
            '(?s)<title>Global history.*'
            '>Global history</.*'
            'List of all <strong>1 changes</strong>.*'
            'Root Article.*no log message.*'
            '</table>'
        )
        self._assertRegex(response.rendered_content, expected)

        URLPath.create_urlpath(URLPath.root(), "testhistory1",
                               title="TestHistory1", content="a page",
                               user_message="Comment 1")
        response = self.c.get(url)
        expected = (
            '(?s)<title>Global history.*'
            '>Global history</.*'
            'List of all <strong>2 changes</strong>.*'
            'TestHistory1.*Comment 1.*'
            'Root Article.*no log message.*'
            '</table>'
        )
        self._assertRegex(response.rendered_content, expected)

        urlpath = URLPath.create_urlpath(
            URLPath.root(),
            "testhistory2",
            title="TestHistory2",
            content="a page",
            user_message="Comment 2"
        )
        expected = (
            '(?s)<title>Global history.*'
            '>Global history</.*'
            'List of all <strong>3 changes</strong>.*'
            'TestHistory2.*Comment 2.*'
            'TestHistory1.*Comment 1.*'
            'Root Article.*no log message.*'
            '</table>'
        )
        response = self.c.get(url)
        self._assertRegex(response.rendered_content, expected)

        response = self.c.get(url0)
        self._assertRegex(response.rendered_content, expected)

        response = self.c.get(url1)
        self._assertRegex(response.rendered_content, expected)

        response = self.c.post(
            reverse('wiki:edit', kwargs={'path': 'testhistory2/'}),
            {'content': 'a page modified',
             'current_revision': str(urlpath.article.current_revision.id),
             'preview': '0',
             'save': '1',
             'summary': 'Testing Revision',
             'title': 'TestHistory2Mod'}
        )

        expected = (
            '(?s)<title>Global history.*'
            '>Global history</.*'
            'List of all <strong>4 changes</strong>.*'
            'TestHistory2Mod.*Testing Revision.*'
            'TestHistory2.*Comment 2.*'
            'TestHistory1.*Comment 1.*'
            'Root Article.*no log message.*'
            '</table>'
        )
        response = self.c.get(url)
        self._assertRegex(response.rendered_content, expected)

        response = self.c.get(url0)
        self._assertRegex(response.rendered_content, expected)

        expected = (
            '(?s)<title>Global history.*'
            '>Global history</.*'
            'List of all <strong>3 changes</strong>.*'
            'TestHistory2Mod.*Testing Revision.*'
            'TestHistory1.*Comment 1.*'
            'Root Article.*no log message.*'
            '</table>'
        )
        response = self.c.get(url1)
        self._assertRegex(response.rendered_content, expected)
