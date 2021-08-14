from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test.testcases import TestCase
from django.urls import re_path
from wiki.conf import settings
from wiki.managers import ArticleManager
from wiki.models import Article
from wiki.models import ArticleRevision
from wiki.models import URLPath
from wiki.urls import WikiURLPatterns

User = get_user_model()
Group = apps.get_model(settings.GROUP_MODEL)


class WikiCustomUrlPatterns(WikiURLPatterns):
    def get_article_urls(self):
        urlpatterns = [
            re_path(
                "^my-wiki/(?P<article_id>[0-9]+)/$",
                self.article_view_class.as_view(),
                name="get",
            ),
        ]
        return urlpatterns

    def get_article_path_urls(self):
        urlpatterns = [
            re_path(
                "^my-wiki/(?P<path>.+/|)$",
                self.article_view_class.as_view(),
                name="get",
            ),
        ]
        return urlpatterns


class ArticleModelTest(TestCase):
    def test_default_fields_of_empty_article(self):

        a = Article.objects.create()

        self.assertIsNone(a.current_revision)
        self.assertIsNone(a.owner)
        self.assertIsNone(a.group)

        self.assertIsNotNone(a.created)
        self.assertIsNotNone(a.modified)

        self.assertIsNotNone(a.group_read)
        self.assertIsNotNone(a.group_write)
        self.assertIsNotNone(a.other_read)
        self.assertIsNotNone(a.other_write)

    # XXX maybe redundant test
    def test_model_manager_class(self):

        self.assertIsInstance(Article.objects, ArticleManager)

    def test_str_method_if_have_current_revision(self):

        title = "Test title"

        a = Article.objects.create()
        ArticleRevision.objects.create(article=a, title=title)

        self.assertEqual(str(a), title)

    def test_str_method_if_dont_have_current_revision(self):

        a = Article.objects.create()

        expected = "Article without content (1)"

        self.assertEqual(str(a), expected)

    def test_get_absolute_url_if_urlpath_set_is_exists(self):

        a1 = Article.objects.create()
        s1 = Site.objects.create(domain="something.com", name="something.com")
        u1 = URLPath.objects.create(article=a1, site=s1)

        a2 = Article.objects.create()
        s2 = Site.objects.create(domain="somethingelse.com", name="somethingelse.com")
        URLPath.objects.create(article=a2, site=s2, parent=u1, slug="test_slug")

        url = a2.get_absolute_url()

        expected = "/test_slug/"

        self.assertEqual(url, expected)

    def test_get_absolute_url_if_urlpath_set_is_not_exists(self):

        a = Article.objects.create()

        url = a.get_absolute_url()

        expected = "/1/"

        self.assertEqual(url, expected)

    def test_article_is_related_to_articlerevision(self):

        title = "Test title"

        a = Article.objects.create()
        r = ArticleRevision.objects.create(article=a, title=title)

        self.assertEqual(r.article, a)
        self.assertIn(r, a.articlerevision_set.all())

    def test_article_is_related_to_owner(self):

        u = User.objects.create(username="Noman", password="pass")
        a = Article.objects.create(owner=u)

        self.assertEqual(a.owner, u)
        self.assertIn(a, u.owned_articles.all())

    def test_article_is_related_to_group(self):

        g = Group.objects.create()
        a = Article.objects.create(group=g)

        self.assertEqual(a.group, g)
        self.assertIn(a, g.article_set.all())

    def test_cache(self):
        a = Article.objects.create()
        ArticleRevision.objects.create(article=a, title="test", content="# header")
        expected = """<h1 id="wiki-toc-header">header""" """.*</h1>"""
        # cached content does not exist yet. this will create it
        self.assertRegexpMatches(a.get_cached_content(), expected)
        # actual cached content test
        self.assertRegexpMatches(a.get_cached_content(), expected)

    def test_articlerevision_presave_signals(self):
        a = Article.objects.create()
        ar1 = ArticleRevision(article=a, title="revision1")

        a.add_revision(ar1)
        self.assertEqual(ar1, a.current_revision)

        ar2 = ArticleRevision(article=a, title="revision2")

        ar2.save()

        self.assertEqual(ar2.previous_revision, ar1)
