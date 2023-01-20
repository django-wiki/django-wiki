import itertools
import re

from django.urls import reverse
from wiki.conf import settings as wiki_settings
from wiki.models import URLPath

from ...base import ArticleWebTestUtils
from ...base import DjangoClientTestBase
from ...base import RequireRootArticleMixin
from ...base import wiki_override_settings
from ...core.test_basic import CustomGroup


class LinkNetworkTests(
    RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase
):
    def setUp(self):
        super().setUp()
        url1 = URLPath.create_urlpath(URLPath.root(), "page1", title="Page 1")
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
        url3b.article.current_revision.content = "[missing](/missing)"

        url1.article.current_revision.save()
        url2.article.current_revision.save()
        url3.article.current_revision.save()
        url3a.article.current_revision.save()
        url3b.article.current_revision.save()
        self.pages = ["Page 1", "Page 2", "Page 3", "Page A", "Page B"]

    def assert_link_counts(self, path, pages, network=True):
        if network:
            url = reverse("wiki:linknetwork", kwargs={"path": path})
        else:
            url = reverse("wiki:whatlinkshere", kwargs={"path": path})
        response = self.client.get(url)
        if network:
            self.assertRegexpMatches(response.rendered_content, ("Link Network"))
        else:
            self.assertRegexpMatches(response.rendered_content, ("What links here"))
        # The different link pairs are expected to be in a table, one row per link.
        rows = response.rendered_content.split("tr>")
        for origin, target in itertools.product(self.pages, repeat=2):
            found = [
                re.search("{}.*{}".format(origin, target), row, re.DOTALL) is not None
                for row in rows
            ]
            assert sum(found) == (1 if (origin, target) in pages else 0)
        for (origin, target) in set.difference(
            pages, itertools.product(self.pages, repeat=2)
        ):
            found = [
                re.search("{}.*{}".format(origin, target), row, re.DOTALL) is not None
                for row in rows
            ]
            assert sum(found) == 1

    def test_linknetwork_global(self):
        self.assert_link_counts(
            "",
            {
                ("Page 1", "Page 2"),
                ("Page 1", "Page 3"),
                ("Page 1", "Page B"),
                ("Page 2", "Page 3"),
                ("Page 3", "Page 1"),
                ("Page 3", "Page A"),
                ("Page 3", "Page B"),
                ("Page A", "Page 1"),
                ("Page A", "Page B"),
                ("Page B", "missing"),
            },
        )

    def test_linknetwork_subwiki(self):
        self.assert_link_counts(
            "page3/",
            {
                ("Page 3", "Page A"),
                ("Page 3", "Page B"),
                ("Page A", "Page B"),
                # NB: The link from Page B to /missing links above Page 3, so
                # it's not part of the hierarchy of /page3 and should not
                # appear here.
            },
        )

    def test_linknetwork_niece(self):
        self.assert_link_counts(
            "page1/",
            {
                ("Page 3", "Page 1"),
                ("Page A", "Page 1"),
            },
            network=False,
        )

    def test_linknetwork_aunt(self):
        self.assert_link_counts(
            "page3/b/",
            {
                ("Page 1", "Page B"),
                ("Page 3", "Page B"),
                ("Page A", "Page B"),
            },
            network=False,
        )


@wiki_override_settings(ACCOUNT_HANDLING=True)
class LinkNetworkPrivilegeTest(LinkNetworkTests):
    def setUp(self):
        super().setUp()

        group = CustomGroup(id=123)
        group.save()

        self.hidden = URLPath.create_urlpath(
            URLPath.root(), "hidden", title="Hidden Page"
        )
        self.hidden.article.other_read = False
        self.hidden.article.owner = self.superuser1
        self.hidden.article.group = group
        self.hidden.article.save()

        self.hidden.article.current_revision.content = (
            "[page2](/page2)[page3](/page3)[page3B](/page3/b)"
        )
        self.hidden.article.current_revision.save()

        self.pages.append("Hidden Page")

        self.client.get(wiki_settings.LOGOUT_URL)

    def test_logged_in_as_superuser(self):
        self.client.force_login(self.superuser1)
        self.assert_link_counts(
            "",
            {
                ("Page 1", "Page 2"),
                ("Page 1", "Page 3"),
                ("Page 1", "Page B"),
                ("Page 2", "Page 3"),
                ("Page 3", "Page 1"),
                ("Page 3", "Page A"),
                ("Page 3", "Page B"),
                ("Page A", "Page 1"),
                ("Page A", "Page B"),
                ("Page B", "missing"),
                ("Hidden Page", "Page 2"),
                ("Hidden Page", "Page 3"),
                ("Hidden Page", "Page B"),
            },
        )
        self.client.get(wiki_settings.LOGOUT_URL)
