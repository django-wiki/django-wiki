from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

import pprint

class InitialWebClientTest(TestCase):
    """Tests by the dummy web client, with manual creating the root article."""

    def setUp(self):
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
        except ImportError:
            from django.contrib.auth.models import User
        
        User.objects.create_superuser('admin', 'nobody@example.com', 'secret')
        self.c = c = Client()
        c.login(username='admin', password='secret')

    def test_root_article(self):
        """Test redirecting to /create-root/, creating the root article and a simple markup."""
        c = self.c
        response = c.get(reverse('wiki:root'))  # url '/'
        self.assertRedirects(response, reverse('wiki:root_create'))  # url '/create-root/'
        response = c.post(reverse('wiki:root_create'),
                {'content': 'test heading h1\n====\n', 'title': 'Wiki Test'})
        self.assertRedirects(response, reverse('wiki:root'))
        response = c.get(reverse('wiki:root'))
        self.assertContains(response, 'test heading h1</h1>')


class WebClientTest(TestCase):
    """Tests by the dummy web client."""
    def setUp(self):
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
        except ImportError:
            from django.contrib.auth.models import User
        User.objects.create_superuser('admin', 'nobody@example.com', 'secret')
        self.c = c = Client()
        c.login(username='admin', password='secret')
        response = self.c.post(reverse('wiki:root_create'), {'content': 'root article content', 'title': 'Root Article'})
        self.example_data = {
                'content': 'The modified text',
                'current_revision': '1',
                'preview': '1',
                #'save': '1',  # probably not too important
                'summary': 'why edited',
                'title': 'wiki test'}

    def tearDown(self):
        # clear Article cache before the next test
        from wiki.models import Article
        Article.objects.all().delete()

    def get_by_path(self, path):
        """Get the article response for the path.
           Example:  self.get_by_path("Level1/Slug2/").title
        """
        return  self.c.get(reverse('wiki:get', kwargs={'path': path}))
    
    def dump_db_status(self, message=''):
        """Debug printing of the complete important database content."""
        print('*** db status *** {}'.format(message))
        from wiki.models import Article, ArticleRevision, URLPath
        for klass in (Article, ArticleRevision, URLPath):
            print('* {} *'.format(klass.__name__))
            pprint.pprint(list(klass.objects.values()), width=240)


    def test_preview_save(self):
        """Test edit preview, edit save and messages."""
        c = self.c
        # test preview
        response = c.post(reverse('wiki:preview', kwargs={'path': ''}), self.example_data)  # url: '/_preview/'
        self.assertContains(response, 'The modified text')
        # test save and messages
        example2 = self.example_data.copy()
        example2['content'] = 'Something 2'
        response = c.post(reverse('wiki:edit', kwargs={'path': ''}), example2)
        message = c.cookies['messages'].value if 'messages' in c.cookies else None
        self.assertRedirects(response, reverse('wiki:root'))
        response = c.get(reverse('wiki:root'))
        #self.dump_db_status('test_preview_save')
        # Why it doesn't display the latest revison text if other test preceded? It is correctly in the db.
        self.assertContains(response, 'Something 2')
        self.assertTrue('succesfully added' in message)

    def test_redirect_create(self):
        """Test that redirects to create if the slug is unknown."""
        response = self.get_by_path('Unknown/')
        self.assertRedirects(response, reverse('wiki:create', kwargs={'path': ''}) + '?slug=Unknown')

    def test_cleared_cache(self):
        """Test the article cache is cleared after delete."""
        # That bug is tested by one individual test, otherwise it could be
        # revealed only by sequence of tests in some particular order
        c = self.c
        response = c.post(reverse('wiki:create', kwargs={'path': ''}),
                {'title': 'Test cache', 'slug': 'TestCache', 'content': 'Content 1'})
        self.assertRedirects(response, reverse('wiki:get', kwargs={'path': 'TestCache/'}))
        response = c.post(reverse('wiki:delete', kwargs={'path': 'TestCache/'}),
                {'confirm': 'on', 'purge': 'on', 'revision': '2'})
        self.assertRedirects(response, reverse('wiki:get', kwargs={'path': ''}))
        response = c.post(reverse('wiki:create', kwargs={'path': ''}),
                {'title': 'Test cache', 'slug': 'TestCache', 'content': 'Content 2'})
        self.assertRedirects(response, reverse('wiki:get', kwargs={'path': 'TestCache/'}))
        # test the cache
        self.assertContains(self.get_by_path('TestCache/'), 'Content 2')

    def test_article_list_update(self):
        """Test automatic adding and removing the new article to/from article_list."""
        c = self.c
        root_data = {'content': '[article_list depth:2]', 'current_revision': '1', 'preview': '1', 'title': 'Root Article'}
        response = c.post(reverse('wiki:edit', kwargs={'path': ''}), root_data)
        self.assertRedirects(response, reverse('wiki:root'))
        # verify the new article is added to article_list
        response = c.post(reverse('wiki:create', kwargs={'path': ''}),
                {'title': 'Sub Article 1', 'slug': 'SubArticle1'})
        self.assertRedirects(response, reverse('wiki:get', kwargs={'path': 'SubArticle1/'}))
        self.assertContains(self.get_by_path(''), 'Sub Article 1')
        self.assertContains(self.get_by_path(''), 'SubArticle1/')
        # verify the deleted article is removed from article_list
        response = c.post(reverse('wiki:delete', kwargs={'path': 'SubArticle1/'}),
                {'confirm': 'on', 'purge': 'on', 'revision': '3'})
        message = c.cookies['messages'].value if 'messages' in c.cookies else None
        self.assertRedirects(response, reverse('wiki:get', kwargs={'path': ''}))
        self.assertTrue('This article together with all its contents are now completely gone' in message)
        self.assertNotContains(self.get_by_path(''), 'Sub Article 1')

    def test_revision_conflict(self):
        """Test the warning if the same article is beeing edited concurrently."""
        c = self.c
        response = c.post(reverse('wiki:edit', kwargs={'path': ''}), self.example_data)
        self.assertRedirects(response, reverse('wiki:root'))
        response = c.post(reverse('wiki:edit', kwargs={'path': ''}), self.example_data)
        self.assertContains(response, 'While you were editing, someone else changed the revision.')
        #self.dump_db_status('after test_revision_conflict')

    def test_nested_create(self):
        c = self.c
        response = c.post(reverse('wiki:create', kwargs={'path': ''}), 
                {'title': 'Level 1', 'slug': 'Level1', 'content': 'Content level 1'})
        self.assertRedirects(response, reverse('wiki:get', kwargs={'path': 'Level1/'}))
        response = c.post(reverse('wiki:create', kwargs={'path': 'Level1/'}), 
                {'title': 'test', 'slug': 'Test', 'content': 'Content on level 2'})
        self.assertRedirects(response, reverse('wiki:get', kwargs={'path': 'Level1/Test/'}))
        response = c.post(reverse('wiki:create', kwargs={'path': ''}), 
                {'title': 'test', 'slug': 'Test', 'content': 'Other content on level 1'})
        self.assertRedirects(response, reverse('wiki:get', kwargs={'path': 'Test/'}))
        self.assertContains(self.get_by_path('Test/'), 'Other content on level 1')
        self.assertContains(self.get_by_path('Level1/Test/'), 'Content') # on level 2')
