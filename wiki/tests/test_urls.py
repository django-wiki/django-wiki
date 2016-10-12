from __future__ import absolute_import, unicode_literals

from django import VERSION as DJANGO_VERSION
from django.conf.urls import url
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test.testcases import TestCase
from django_nyt.urls import get_pattern as get_notify_pattern
from wiki.models import Article, URLPath
from wiki.tests.base import wiki_override_settings
from wiki.urls import get_pattern as get_wiki_pattern
from wiki.urls import WikiURLPatterns

User = get_user_model()


class WikiCustomUrlPatterns(WikiURLPatterns):

    def get_article_urls(self):
        urlpatterns = [
            url('^some-prefix/(?P<article_id>\d+)/$',
                self.article_view_class.as_view(),
                name='get'
                ),
        ]
        return urlpatterns

    def get_article_path_urls(self):
        urlpatterns = [
            url('^some-other-prefix/(?P<path>.+/|)$',
                self.article_view_class.as_view(),
                name='get'),
        ]
        return urlpatterns

urlpatterns = [
    url(r'^notify/', get_notify_pattern()),
    url(r'', get_wiki_pattern(url_config_class=WikiCustomUrlPatterns))
]


@wiki_override_settings(WIKI_URL_CONFIG_CLASS='wiki.tests.test_models.WikiCustomUrlPatterns',
                        ROOT_URLCONF='wiki.tests.test_urls')
class ArticleModelReverseMethodTest(TestCase):

    if DJANGO_VERSION < (1, 7):
        urls = 'wiki.tests.test_urls'

    def test_get_absolute_url_if_urlpath_set_is_not_exists__no_root_urlconf(self):
        a = Article.objects.create()

        url = a.get_absolute_url()

        expected = '/some-prefix/1/'

        self.assertEqual(url, expected)

    def test_get_absolute_url_if_urlpath_set_is_exists__no_root_urlconf(self):

        a1 = Article.objects.create()
        s1 = Site.objects.create(domain="something.com", name="something.com")
        u1 = URLPath.objects.create(article=a1, site=s1)

        a2 = Article.objects.create()
        s2 = Site.objects.create(domain="somethingelse.com", name="somethingelse.com")
        URLPath.objects.create(
            article=a2,
            site=s2,
            parent=u1,
            slug='test_slug'
        )

        url = a2.get_absolute_url()

        expected = '/some-other-prefix/test_slug/'

        self.assertEqual(url, expected)
