from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.template import Context, Template
from django.test.utils import override_settings

from wiki.models import URLPath


class WebTestBase(TestCase):

    def setUp(self):

        super(TestCase, self).setUp()

        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
        except ImportError:
            from django.contrib.auth.models import User

        self.superuser1 = User.objects.create_superuser(
            'admin',
            'nobody@example.com',
            'secret'
        )

        self.c = c = Client()
        c.login(username='admin', password='secret')


class ArticleTestBase(WebTestBase):

    """Base class for web client tests, that sets up initial root article."""

    def setUp(self):

        super(ArticleTestBase, self).setUp()

        response = self.c.post(
            reverse('wiki:root_create'),
            {'content': 'root article content', 'title': 'Root Article'},
            follow=True
        )

        self.assertEqual(response.status_code, 200)  # sanity check
        self.root_article = URLPath.root().article
        self.example_data = {
            'content': 'The modified text',
            'current_revision': '1',
            'preview': '1',
            # 'save': '1',  # probably not too important
            'summary': 'why edited',
            'title': 'wiki test'
        }

    def get_by_path(self, path):
        """
        Get the article response for the path.
        Example:  self.get_by_path("Level1/Slug2/").title
        """

        return self.c.get(reverse('wiki:get', kwargs={'path': path}))


class BaseTestCase(TestCase):

    @property
    def template(self):
        raise Exception("Not implemented")

    def render(self, template, context):
        return Template(template).render(Context(context))


class wiki_override_settings(override_settings):

    def __enter__(self):
        super(wiki_override_settings, self).__enter__()

        from imp import reload
        from wiki.conf import settings
        reload(settings)
