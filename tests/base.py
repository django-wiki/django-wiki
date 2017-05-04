from __future__ import absolute_import, unicode_literals

import os
import unittest

import django_functest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.template import Context, Template
from django.test import TestCase
from django.test.client import Client

from wiki.models import URLPath

try:
    from django.test import override_settings
except ImportError:
    from django.test.utils import override_settings



SUPERUSER1_USERNAME = 'admin'
SUPERUSER1_PASSWORD = 'secret'


class RequireSuperuserMixin(object):

    def setUp(self):
        super(RequireSuperuserMixin, self).setUp()

        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
        except ImportError:
            from django.contrib.auth.models import User

        self.superuser1 = User.objects.create_superuser(
            SUPERUSER1_USERNAME,
            'nobody@example.com',
            SUPERUSER1_PASSWORD
        )


class RequireBasicData(RequireSuperuserMixin):
    """
    Mixin that creates common data required for all tests.
    """
    pass


class TestBase(RequireBasicData, TestCase):
    pass


class RequireRootArticleMixin(object):

    def setUp(self):
        super(RequireRootArticleMixin, self).setUp()
        self.root = URLPath.create_root()
        self.root_article = URLPath.root().article
        rev = self.root_article.current_revision
        rev.title = "Root Article"
        rev.content = "root article content"
        rev.save()


class ArticleTestBase(RequireRootArticleMixin, TestBase):
    """
    Sets up basic data for testing with an article and some revisions
    """
    pass


class DjangoClientTestBase(TestBase):
    def setUp(self):
        super(DjangoClientTestBase, self).setUp()

        self.c = c = Client()
        c.login(username=SUPERUSER1_USERNAME, password=SUPERUSER1_PASSWORD)



class WebTestCommonMixin(RequireBasicData, django_functest.ShortcutLoginMixin):
    """
    Common setup required for WebTest and Selenium tests
    """
    def setUp(self):
        super(WebTestCommonMixin, self).setUp()

        self.shortcut_login(username=SUPERUSER1_USERNAME,
                            password=SUPERUSER1_PASSWORD)


class WebTestBase(WebTestCommonMixin, django_functest.FuncWebTestMixin, TestCase):
    pass


INCLUDE_SELENIUM_TESTS = os.environ.get('INCLUDE_SELENIUM_TESTS', '0') == '1'


@unittest.skipIf(not INCLUDE_SELENIUM_TESTS, "Skipping Selenium tests")
class SeleniumBase(WebTestCommonMixin, django_functest.FuncSeleniumMixin, StaticLiveServerTestCase):
    driver_name = "Chrome"
    display = os.environ.get('SELENIUM_SHOW_BROWSER', '0') == '1'

    if not INCLUDE_SELENIUM_TESTS:
        # Don't call super() in setUpClass(), it will attempt to instatiate
        # a browser instance which is slow and might fail
        @classmethod
        def setUpClass(cls):
            pass

        @classmethod
        def tearDownClass(cls):
            pass


class ArticleWebTestUtils(object):

    def get_by_path(self, path):
        """
        Get the article response for the path.
        Example:  self.get_by_path("Level1/Slug2/").title
        """

        return self.c.get(reverse('wiki:get', kwargs={'path': path}))


class TemplateTestCase(TestCase):

    @property
    def template(self):
        raise Exception("Not implemented")

    def render(self, context):
        return Template(self.template).render(Context(context))


# See
# https://github.com/django-wiki/django-wiki/pull/382
class wiki_override_settings(override_settings):

    def enable(self):
        super(wiki_override_settings, self).enable()
        self.reload_wiki_settings()

    def disable(self):
        super(wiki_override_settings, self).disable()
        self.reload_wiki_settings()

    def reload_wiki_settings(self):
        from imp import reload
        from wiki.conf import settings
        reload(settings)
