from importlib import reload

from django.contrib.sites.models import Site
from django.test.testcases import TestCase
from wiki import sites, urls
from wiki.apps import WikiConfig
from wiki.compat import include, url
from wiki.models import Article, URLPath

from ..base import wiki_override_settings


class WikiCustomSite(sites.WikiSite):
    def get_article_urls(self):
        urlpatterns = [
            url('^some-prefix/(?P<article_id>[0-9]+)/$', self.article_view, name='get'),
        ]
        return urlpatterns

    def get_article_path_urls(self):
        urlpatterns = [
            url('^some-other-prefix/(?P<path>.+/|)$', self.article_view, name='get'),
        ]
        return urlpatterns


class WikiCustomConfig(WikiConfig):
    default_site = "tests.core.test_sites.WikiCustomSite"


urlpatterns = [
    url(r'^notify/', include('django_nyt.urls')),
    url(r'', include('wiki.urls')),
]


@wiki_override_settings(
    INSTALLED_APPS=[
        'tests.testdata',
        'django.contrib.auth.apps.AuthConfig',
        'django.contrib.contenttypes.apps.ContentTypesConfig',
        'django.contrib.sessions.apps.SessionsConfig',
        'django.contrib.admin.apps.AdminConfig',
        'django.contrib.humanize.apps.HumanizeConfig',
        'django.contrib.sites.apps.SitesConfig',
        'django_nyt.apps.DjangoNytConfig',
        'mptt',
        'sekizai',
        'sorl.thumbnail',
        'tests.core.test_sites.WikiCustomConfig',
        'wiki.plugins.attachments.apps.AttachmentsConfig',
        'wiki.plugins.notifications.apps.NotificationsConfig',
        'wiki.plugins.images.apps.ImagesConfig',
        'wiki.plugins.macros.apps.MacrosConfig',
        'wiki.plugins.globalhistory.apps.GlobalHistoryConfig',
    ],
    ROOT_URLCONF='tests.core.test_sites',
)
class CustomWikiSiteTest(TestCase):
    def setUp(self):
        # Reload wiki.urls since it may have already been instantiated by another test app.
        self._old_site = sites.site
        sites.site = sites.DefaultWikiSite()
        reload(urls)

    def tearDown(self):
        sites.site = self._old_site
        reload(urls)

    def test_use_custom_wiki_site(self):
        self.assertEqual(sites.site.__class__.__name__, 'WikiCustomSite')

    def test_get_absolute_url_if_urlpath_set_is_not_exists__no_root_urlconf(self):
        a = Article.objects.create()

        self.assertEqual(a.get_absolute_url(), '/some-prefix/1/')

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

        self.assertEqual(a2.get_absolute_url(), '/some-other-prefix/test_slug/')
