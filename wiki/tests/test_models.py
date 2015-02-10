from __future__ import unicode_literals
from __future__ import absolute_import

from django.test.testcases import TestCase
from django.contrib.sites.models import Site
from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()

from wiki.models import (
    Article,
    ArticleRevision,
    ArticleForObject,
    BaseRevisionMixin,
    URLPath
)

from wiki.tests.base import wiki_override_settings
from wiki.managers import ArticleManager


class ArticleModelTest(TestCase):

    def test_default_fields_of_empty_article(self):

        a = Article.objects.create()

        self.assertFalse(a.current_revision)
        self.assertFalse(a.owner)
        self.assertFalse(a.group)

        self.assertTrue(a.created)
        self.assertTrue(a.modified)

        self.assertTrue(a.group_read)
        self.assertTrue(a.group_write)
        self.assertTrue(a.other_read)
        self.assertTrue(a.other_write)


    # XXX maybe is redundant test
    def test_model_manager_class(self):

        self.assertTrue(isinstance(Article.objects, ArticleManager))

    def test_str_method_if_have_current_revision(self):

        title = 'Test title'

        a = Article.objects.create()
        r = ArticleRevision.objects.create(article=a, title=title)

        self.assertEqual(str(a), title)

    def test_str_method_if_dont_have_current_revision(self):

        a = Article.objects.create()

        expected = 'Article without content (1)'

        self.assertEqual(str(a), expected)

    # TODO looks tricky
    def test_get_absolute_url_if_urlpath_set_is_exists(self):

        # a = Article.objects.create()
        # s = Site.objects.create()

        # URLPath.objects.create(article=a, site=s)
        pass


    def test_get_absolute_url_if_urlpath_set_is_not_exists(self):

        a = Article.objects.create()

        expected = '/1/'

        url = a.get_absolute_url()

        self.assertEqual(url, expected)

    def test_article_is_related_to_articlerevision(self):

        title = 'Test title'

        a = Article.objects.create()
        r = ArticleRevision.objects.create(article=a, title=title)

        self.assertEqual(r.article, a)
        self.assertIn(r, a.articlerevision_set.all())

    def test_article_is_related_to_owner(self):

        u = User.objects.create(username='Noman', password='pass')
        a = Article.objects.create(owner=u)

        self.assertEqual(a.owner, u)
        self.assertIn(a, u.owned_articles.all())

    def test_article_is_related_to_group(self):

        g = Group.objects.create()
        a = Article.objects.create(group=g)

        self.assertEqual(a.group, g)
        self.assertIn(a, g.article_set.all())


class ArticleRevisionModelTest(TestCase):

    def test_some(self):
        pass
