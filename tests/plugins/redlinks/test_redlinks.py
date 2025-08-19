from django.urls import reverse
from wiki.core import markdown
from wiki.models import URLPath

from ...base import wiki_override_settings
from tests.base import RequireRootArticleMixin
from tests.base import TestBase


class RedlinksTests(RequireRootArticleMixin, TestBase):
    def setUp(self):
        super().setUp()
        self.child = URLPath.create_urlpath(self.root, "child")

    def test_root_to_self(self):
        self.assert_internal(self.root, "[Internal](./)")

    def test_root_to_child(self):
        self.assert_internal(self.root, "[Child](child/)")

    def test_child_to_self(self):
        self.assert_internal(self.child, "[Child](../child/)")

    def test_child_to_self_no_slash(self):
        self.assert_internal(self.child, "[Child](../child)")

    def test_root_to_outside(self):
        self.assert_external(
            self.root, "[Outside](http://outside.example.org/)"
        )

    def test_absolute_external(self):
        if reverse("wiki:get", kwargs={"path": ""}) == "/":
            # All absolute paths could be wiki-internal, and the server root is
            # the the wiki root, which is bound to exist.
            self.assert_internal(self.root, "[Server Root](/)")
        else:
            # The wiki root is below the server root, so the server root is an
            # external link.
            self.assert_external(self.root, "[Server Root](/)")
            self.assert_external(self.root, "[Static File](/static/)")

    def test_absolute_internal(self):
        wiki_root = reverse("wiki:get", kwargs={"path": ""})
        self.assert_internal(self.root, f"[Server Root]({wiki_root})")

    def test_child_to_broken(self):
        self.assert_broken(self.child, "[Broken](../broken/)")

    def test_root_to_broken(self):
        self.assert_broken(self.root, "[Broken](broken/)")

    def test_not_a_link(self):
        self.assert_none(self.root, '<a id="anchor">old-style anchor</a>')

    def test_invalid_url(self):
        self.assert_none(self.root, "[Invalid](http://127[.500.20.1/)")

    def test_mailto(self):
        self.assert_none(self.root, "<foo@example.com>")

    def assert_none(self, urlpath, md_text):
        md = markdown.ArticleMarkdown(article=urlpath.article)
        html = md.convert(md_text)
        self.assertNotIn("wiki-internal", html)
        self.assertNotIn("wiki-external", html)
        self.assertNotIn("wiki-broken", html)
        self.assertIn("<a", html)

    def assert_internal(self, urlpath, md_text):
        md = markdown.ArticleMarkdown(article=urlpath.article)
        html = md.convert(md_text)
        self.assertIn("wiki-internal", html)
        self.assertNotIn("wiki-external", html)
        self.assertNotIn("wiki-broken", html)

    def assert_external(self, urlpath, md_text):
        md = markdown.ArticleMarkdown(article=urlpath.article)
        html = md.convert(md_text)
        self.assertNotIn("wiki-internal", html)
        self.assertIn("wiki-external", html)
        self.assertNotIn("wiki-broken", html)

    def assert_broken(self, urlpath, md_text):
        md = markdown.ArticleMarkdown(article=urlpath.article)
        html = md.convert(md_text)
        self.assertNotIn("wiki-internal", html)
        self.assertNotIn("wiki-external", html)
        self.assertIn("wiki-broken", html)


@wiki_override_settings(
    WIKI_URL_CONFIG_CLASS="tests.core.test_models.WikiCustomUrlPatterns",
    ROOT_URLCONF="tests.core.test_urls",
)
class RedLinksWithChangedBaseURL(RedlinksTests):
    pass
