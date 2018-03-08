from unittest import mock

from django.contrib.sites.models import Site
from django.db.models.signals import pre_delete
from django.test import override_settings

from tests.base import RequireRootArticleMixin, TestBase
from wiki.models import Article, ArticleRevision, URLPath


class DeleteSignalTests(RequireRootArticleMixin, TestBase):
    def setUp(self):
        super().setUp()
        self.site = Site.objects.get()
        self.a1 = Article.objects.create()
        self.a2 = Article.objects.create()
        # make some revisions so it's easier to test
        ArticleRevision.objects.create(
            article=self.a1, content='Just material', title='Just title',
        )
        ArticleRevision.objects.create(
            article=self.a2, content='Just material', title='Just title',
        )
        self.fake_root_article = Article.objects.create()
        self.fake_root = URLPath.objects.create(
            site=self.site, slug='new', parent=self.root, article=self.fake_root_article,
        )
        self.a1_urlpath = URLPath.objects.create(
            site=self.site, slug='rock', parent=self.fake_root, article=self.a1,
        )
        self.a2_urlpath = URLPath.objects.create(
            site=self.site, slug='roll', parent=self.fake_root, article=self.a2,
        )

    @override_settings(LOST_AND_FOUND_SLUG='lost')
    def test_delete_root_with_settings(self):
        with mock.patch('wiki.models.urlpath.on_article_delete', autospec=True) as signal:
            pre_delete.connect(signal, sender=Article)
            self.fake_root_article.delete()
        self.assertEqual(signal.call_count, 1)
        # self.assertEqual(self.a1.urlpath_set.all().count(), 1)
        print(self.a1.urlpath_set.all(), self.a2.urlpath_set.all())

    # @override_settings(LOST_AND_FOUND_SLUG=None)
    # def test_delete_root(self):
    #     self.sub_urlpath.delete()
    #     self.assertEqual(self.a1)
