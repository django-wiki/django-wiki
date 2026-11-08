from unittest import mock

from wiki.conf import settings as wiki_settings
from wiki.core import markdown
from wiki.models import URLPath

from tests.base import RequireRootArticleMixin
from tests.base import TestBase


class WikiLinksTests(RequireRootArticleMixin, TestBase):
    def convert(self, text, article=None):
        md = markdown.ArticleMarkdown(article=article or self.root_article)
        return md.convert(text)

    def test_wikilink(self):
        self.assertEqual(
            self.convert("[[Root Article]]"),
            '<p><a class="wiki_wikilink wiki-broken" href="/root-article/">Root Article</a></p>',
        )

    def test_wikilink_matches_suggested_slug(self):
        # "My Article Title" is suggested the slug "my-article-title" when an
        # article is created with that title.
        URLPath.create_urlpath(self.root, "my-article-title")
        self.assertEqual(
            self.convert("[[My Article Title]]"),
            '<p><a class="wiki_wikilink wiki-internal" href="my-article-title/">My Article Title</a></p>',
        )

    def test_wikilink_collapses_spaces_and_hyphens(self):
        URLPath.create_urlpath(self.root, "my-article-title")
        self.assertEqual(
            self.convert("[[My  Article - Title]]"),
            '<p><a class="wiki_wikilink wiki-internal" href="my-article-title/">My  Article - Title</a></p>',
        )

    def test_wikilink_to_underscore_slug(self):
        # Articles created with the slug format previously produced by
        # wikilinks are still linked to.
        URLPath.create_urlpath(self.root, "legacy_page")
        self.assertEqual(
            self.convert("[[Legacy Page]]"),
            '<p><a class="wiki_wikilink wiki-internal" href="legacy_page/">Legacy Page</a></p>',
        )

    def test_wikilink_from_child_article(self):
        child = URLPath.create_urlpath(self.root, "child")
        URLPath.create_urlpath(child, "my-article-title")
        self.assertEqual(
            self.convert("[[My Article Title]]", article=child.article),
            '<p><a class="wiki_wikilink wiki-internal" href="my-article-title/">My Article Title</a></p>',
        )

    def test_wikilink_from_child_article_to_root_level(self):
        child = URLPath.create_urlpath(self.root, "child")
        URLPath.create_urlpath(self.root, "my-article-title")
        self.assertEqual(
            self.convert("[[My Article Title]]", article=child.article),
            '<p><a class="wiki_wikilink wiki-internal" href="/my-article-title/">My Article Title</a></p>',
        )

    @mock.patch.object(wiki_settings, "URL_CASE_SENSITIVE", True)
    def test_wikilink_case_sensitive(self):
        URLPath.create_urlpath(self.root, "Legacy_Page")
        self.assertEqual(
            self.convert("[[Legacy Page]]"),
            '<p><a class="wiki_wikilink wiki-internal" href="Legacy_Page/">Legacy Page</a></p>',
        )
        self.assertEqual(
            self.convert("[[Other Page]]"),
            '<p><a class="wiki_wikilink wiki-broken" href="/other-page/">Other Page</a></p>',
        )
