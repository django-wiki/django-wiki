from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from wiki.models import URLPath


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
            follow=True)
        self.assertEqual(response.status_code, 200)  # sanity check
        self.root_article = URLPath.root().article
        self.example_data = {
            'content': 'The modified text',
            'current_revision': '1',
            'preview': '1',
            # 'save': '1',  # probably not too important
            'summary': 'why edited',
            'title': 'wiki test'}

    def get_by_path(self, path):
        """Get the article response for the path.
           Example:  self.get_by_path("Level1/Slug2/").title
        """
        return self.c.get(reverse('wiki:get', kwargs={'path': path}))
