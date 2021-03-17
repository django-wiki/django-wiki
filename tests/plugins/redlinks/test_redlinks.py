from django.urls import reverse
from wiki.core import markdown
from wiki.models import URLPath

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
        self.assert_external(self.root, "[Outside](http://outside.example.org/)")

    def test_absolute_external(self):
        if reverse("wiki:get", kwargs={"path": ""}) == "/":
            # All absolute paths could be wiki-internal, and the server root is
            # the the wiki root, which is bound to exist.
            self.assert_internal(self.root, "[Server Root](/)")
        else:
            # The wiki root is below the server root, so the server root is an
            # external link.
            self.assert_external(self.root, "[Server Root](/)")

    def test_child_to_broken(self):
        self.assert_broken(self.child, "[Broken](../broken/)")

    def test_root_to_broken(self):
        self.assert_broken(self.root, "[Broken](broken/)")

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

    def test_mailto(self):
        md = markdown.ArticleMarkdown(article=self.root.article)
        md_text = "<foo@example.com>"
        html = md.convert(md_text)
        self.assertNotIn("wiki-internal", html)
        self.assertNotIn("wiki-external", html)
        self.assertNotIn("wiki-broken", html)
        self.assertIn("<a ", html)
