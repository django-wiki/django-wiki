from __future__ import print_function, unicode_literals

import sys

from django.core.urlresolvers import reverse
from wiki.models import URLPath
from ...base import ArticleWebTestBase

class GlobalhistoryTests(ArticleWebTestBase):

    def _assertRegex(self, a, b):
        if sys.version_info >= (3, 2):
            return self.assertRegex(a, b)
        else:
            return self.assertRegexpMatches(a, b)

    def setUp(self):
        super(GlobalhistoryTests, self).setUp()

    def test_history(self):
        url = reverse('wiki:globalhistory')

        response = self.c.get(url)
        expected = (
            '(?s)<title>Global history.*'
            '>Global history</.*'
            'List of all <strong>1 changes</strong>.*'
            'Root Article.*no log message.*'
            '</table>'
        )
        self._assertRegex(response.rendered_content, expected)

        URLPath.create_article(URLPath.root(), "testhistory1",
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

        URLPath.create_article(URLPath.root(), "testhistory2",
                               title="TestHistory2", content="a page",
                               user_message="Comment 2")
        response = self.c.get(url)
        expected = (
            '(?s)<title>Global history.*'
            '>Global history</.*'
            'List of all <strong>3 changes</strong>.*'
            'TestHistory2.*Comment 2.*'
            'TestHistory1.*Comment 1.*'
            'Root Article.*no log message.*'
            '</table>'
        )
        self._assertRegex(response.rendered_content, expected)
