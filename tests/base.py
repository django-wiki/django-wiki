from __future__ import absolute_import, unicode_literals

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


class TestBase(TestCase):
    """
    Sets up basic data
    """

    def setUp(self):

        super(TestCase, self).setUp()

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


class ArticleTestBase(TestCase):
    """
    Sets up basic data for testing with an article and some revisions
    """

    def setUp(self):

        super(ArticleTestBase, self).setUp()

        self.root = URLPath.create_root()
        self.child1 = URLPath.create_article(self.root, 'test-slug', title="Test 1")


class WebTestBase(TestBase):

    def setUp(self):
        """Login as the superuser created because we shall access restricted
        views"""

        super(WebTestBase, self).setUp()

        self.c = c = Client()
        c.login(username=SUPERUSER1_USERNAME, password=SUPERUSER1_PASSWORD)


class ArticleWebTestBase(WebTestBase):

    """Base class for web client tests, that sets up initial root article."""

    def setUp(self):

        super(ArticleWebTestBase, self).setUp()

        response = self.c.post(
            reverse('wiki:root_create'),
            {'content': 'root article content', 'title': 'Root Article'},
            follow=True
        )

        self.assertEqual(response.status_code, 200)  # sanity check
        self.root_article = URLPath.root().article

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
