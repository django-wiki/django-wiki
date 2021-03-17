import re

from django.urls import reverse
from wiki.models import URLPath

from ...base import ArticleWebTestUtils
from ...base import DjangoClientTestBase
from ...base import RequireRootArticleMixin


class WhatLinksWhereTests(
    RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase
):
    def setUp(self):
        super().setUp()
        url1 = URLPath.create_urlpath(
            URLPath.root(),
            "page1",
            title="Page 1",
        )
        url2 = URLPath.create_urlpath(URLPath.root(), "page2", title="Page 2")
        url3 = URLPath.create_urlpath(URLPath.root(), "page3", title="Page 3")
        url3a = URLPath.create_urlpath(url3, "a", title="Page A")
        url3b = URLPath.create_urlpath(url3, "b", title="Page B")

        url1.article.current_revision.content = (
            "[page2](/page2)[page3](/page3)[page3B](/page3/b)"
        )
        url2.article.current_revision.content = "[page3](/page3)"
        url3.article.current_revision.content = (
            "[page1](/page1) [page3A](a) [page3B](b)"
        )
        url3a.article.current_revision.content = "[page1](/page1) [page3B](../b)"
        url3b.article.current_revision.content = "No links"

        url1.article.current_revision.save()
        url2.article.current_revision.save()
        url3.article.current_revision.save()
        url3a.article.current_revision.save()
        url3b.article.current_revision.save()

    # All these tests are very similar, with more similar tests to come for
    # different user permissions, etc.. TODO: Tie them all together in a common
    # function that only takes the 'here' vs. 'there', the anchor article, and
    # the list of links expected to be present (and tests the product for
    # absence).
    def test_whatlinkswhere_global(self):
        url = reverse("wiki:whatlinkswhere", kwargs={"path": ""})
        response = self.client.get(url)
        self.assertRegexpMatches(response.rendered_content, ("What links where"))
        # The different link pairs are expected to be in a table, one row per link.
        rows = response.rendered_content.split("tr>")
        for pages in [
            ("Page 1", "Page 2"),
            ("Page 1", "Page 3"),
            ("Page 1", "Page B"),
            ("Page 2", "Page 3"),
            ("Page 3", "Page 1"),
            ("Page 3", "Page A"),
            ("Page 3", "Page B"),
            ("Page A", "Page 1"),
            ("Page A", "Page B"),
        ]:
            found = [
                re.search(f"{pages[0]}.*{pages[1]}", row, re.DOTALL) is not None
                for row in rows
            ]
            assert sum(found) == 1
            del rows[found.index(True)]

    def test_whatlinkswhere_subwiki(self):
        url = reverse("wiki:whatlinkswhere", kwargs={"path": "page3/"})
        response = self.client.get(url)
        self.assertRegexpMatches(response.rendered_content, ("What links where"))
        # The different link pairs are expected to be in a table, one row per link.
        rows = response.rendered_content.split("tr>")
        for pages in [
            ("Page 1", "Page 2", 0),
            ("Page 1", "Page 3", 0),
            ("Page 1", "Page B", 0),
            ("Page 2", "Page 3", 0),
            ("Page 3", "Page 1", 0),
            ("Page 3", "Page A", 1),
            ("Page 3", "Page B", 1),
            ("Page A", "Page 1", 0),
            ("Page A", "Page B", 1),
        ]:
            found = [
                re.search(f"{pages[0]}.*{pages[1]}", row, re.DOTALL) is not None
                for row in rows
            ]
            assert sum(found) == pages[2]
            if sum(found):
                del rows[found.index(True)]

    def test_whatlinkshere_niece(self):
        url = reverse("wiki:whatlinkshere", kwargs={"path": "page1/"})
        response = self.client.get(url)
        self.assertRegexpMatches(response.rendered_content, ("What links here"))
        # The different link pairs are expected to be in a table, one row per link.
        rows = response.rendered_content.split("tr>")
        for pages in [
            ("Page 3", "Page 1"),
            ("Page A", "Page 1"),
        ]:
            found = [
                re.search(f"{pages[0]}.*{pages[1]}", row, re.DOTALL) is not None
                for row in rows
            ]
            assert sum(found) == 1
            del rows[found.index(True)]

    def test_whatlinkshere_aunt(self):
        url = reverse("wiki:whatlinkshere", kwargs={"path": "page3/b/"})
        response = self.client.get(url)
        self.assertRegexpMatches(response.rendered_content, ("What links here"))
        # The different link pairs are expected to be in a table, one row per link.
        rows = response.rendered_content.split("tr>")
        for pages in [
            ("Page 1", "Page B"),
            ("Page 3", "Page B"),
            ("Page A", "Page B"),
        ]:
            found = [
                re.search(f"{pages[0]}.*{pages[1]}", row, re.DOTALL) is not None
                for row in rows
            ]
            assert sum(found) == 1
            del rows[found.index(True)]
