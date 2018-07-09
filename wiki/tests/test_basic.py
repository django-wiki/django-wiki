from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from django.core.urlresolvers import reverse

import pprint

from .base import ArticleTestBase, WebTestBase

from wiki import models
from wiki.plugins.attachments.models import Attachment


class ModelTests(ArticleTestBase):
    """Tests basic model and queryset functionalities"""
    
    def test_custom_querysets(self):
        """
        Tests that the custom queryset methods work, this is important
        because the pattern of building them is different from Django
        1.5 to 1.6 to 1.7 so there will be 3 patterns in play at the
        same time.
        """
        
        # Test methods directly on manager
        self.assertEqual(models.Article.objects.can_read(self.superuser1).count(), 1)
        self.assertEqual(models.Article.objects.can_write(self.superuser1).count(), 1)
        self.assertEqual(models.Article.objects.active().count(), 1)
        
        # Test methods on querysets
        self.assertEqual(models.Article.objects.all().can_read(self.superuser1).count(), 1)
        self.assertEqual(models.Article.objects.all().can_write(self.superuser1).count(), 1)
        self.assertEqual(models.Article.objects.all().active().count(), 1)

        # Test empty query sets
        # See: https://code.djangoproject.com/ticket/22817
        self.assertEqual(models.Article.objects.none().can_read(self.superuser1).count(), 0)
        self.assertEqual(models.Article.objects.none().can_write(self.superuser1).count(), 0)
        self.assertEqual(models.Article.objects.none().active().count(), 0)

        # Do the same for Attachment which uses ArtickeFkManager
        # Test methods directly on manager
        self.assertEqual(Attachment.objects.can_read(self.superuser1).count(), 0)
        self.assertEqual(Attachment.objects.can_write(self.superuser1).count(), 0)
        self.assertEqual(Attachment.objects.active().count(), 0)
        
        # Test methods on querysets
        self.assertEqual(Attachment.objects.all().can_read(self.superuser1).count(), 0)
        self.assertEqual(Attachment.objects.all().can_write(self.superuser1).count(), 0)
        self.assertEqual(Attachment.objects.all().active().count(), 0)

        # Test empty query sets
        # See: https://code.djangoproject.com/ticket/22817
        self.assertEqual(Attachment.objects.none().can_read(self.superuser1).count(), 0)
        self.assertEqual(Attachment.objects.none().can_write(self.superuser1).count(), 0)
        self.assertEqual(Attachment.objects.none().active().count(), 0)


class RootArticleViewTests(WebTestBase):

    """Tests for creating/viewing the root article."""

    def test_root_article(self):
        """Test redirecting to /create-root/, creating the root article and a simple markup."""
        c = self.c
        response = c.get(reverse('wiki:root'))  # url '/'
        self.assertRedirects(
            response,
            reverse('wiki:root_create'))  # url '/create-root/'
        response = c.post(
            reverse('wiki:root_create'), {
                'content': 'test heading h1\n====\n', 'title': 'Wiki Test'})
        self.assertRedirects(response, reverse('wiki:root'))
        response = c.get(reverse('wiki:root'))
        self.assertContains(response, 'test heading h1</h1>')


class ArticleViewTests(ArticleTestBase):

    """
    Tests for article views, assuming a root article already created.
    """

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
        response = c.post(
            reverse(
                'wiki:preview',
                kwargs={
                    'path': ''}),
            self.example_data)  # url: '/_preview/'
        self.assertContains(response, 'The modified text')
        # test save and messages
        example2 = self.example_data.copy()
        example2['content'] = 'Something 2'
        response = c.post(reverse('wiki:edit', kwargs={'path': ''}), example2)
        message = c.cookies[
            'messages'].value if 'messages' in c.cookies else None
        self.assertRedirects(response, reverse('wiki:root'))
        response = c.get(reverse('wiki:root'))
        # self.dump_db_status('test_preview_save')
        # Why it doesn't display the latest revison text if other test
        # preceded? It is correctly in the db.
        self.assertContains(response, 'Something 2')
        self.assertTrue('succesfully added' in message)

    def test_redirect_create(self):
        """Test that redirects to create if the slug is unknown."""
        response = self.get_by_path('Unknown/')
        self.assertRedirects(
            response,
            reverse(
                'wiki:create',
                kwargs={
                    'path': ''}) +
            '?slug=Unknown')

    def test_cleared_cache(self):
        """Test the article cache is cleared after delete."""
        # That bug is tested by one individual test, otherwise it could be
        # revealed only by sequence of tests in some particular order
        c = self.c
        response = c.post(
            reverse(
                'wiki:create', kwargs={
                    'path': ''}), {
                'title': 'Test cache', 'slug': 'testcache', 'content': 'Content 1'})
        self.assertRedirects(
            response,
            reverse(
                'wiki:get',
                kwargs={
                    'path': 'testcache/'}))
        response = c.post(
            reverse('wiki:delete', kwargs={'path': 'testcache/'}),
            {'confirm': 'on', 'purge': 'on', 'revision': '2'})
        self.assertRedirects(
            response,
            reverse(
                'wiki:get',
                kwargs={
                    'path': ''}))
        response = c.post(
            reverse(
                'wiki:create', kwargs={
                    'path': ''}), {
                'title': 'Test cache', 'slug': 'TestCache', 'content': 'Content 2'})
        self.assertRedirects(
            response,
            reverse(
                'wiki:get',
                kwargs={
                    'path': 'testcache/'}))
        # test the cache
        self.assertContains(self.get_by_path('TestCache/'), 'Content 2')

    def test_article_list_update(self):
        """Test automatic adding and removing the new article to/from article_list."""
        c = self.c
        root_data = {
            'content': '[article_list depth:2]',
            'current_revision': '1',
            'preview': '1',
            'title': 'Root Article'}
        response = c.post(reverse('wiki:edit', kwargs={'path': ''}), root_data)
        self.assertRedirects(response, reverse('wiki:root'))
        # verify the new article is added to article_list
        response = c.post(reverse('wiki:create', kwargs={'path': ''}),
                          {'title': 'Sub Article 1', 'slug': 'SubArticle1'})
        self.assertRedirects(
            response,
            reverse(
                'wiki:get',
                kwargs={
                    'path': 'subarticle1/'}))
        self.assertContains(self.get_by_path(''), 'Sub Article 1')
        self.assertContains(self.get_by_path(''), 'subarticle1/')
        # verify the deleted article is removed from article_list
        response = c.post(
            reverse('wiki:delete', kwargs={'path': 'SubArticle1/'}),
            {'confirm': 'on', 'purge': 'on', 'revision': '3'})
        message = c.cookies[
            'messages'].value if 'messages' in c.cookies else None
        self.assertRedirects(
            response,
            reverse(
                'wiki:get',
                kwargs={
                    'path': ''}))
        self.assertTrue(
            'This article together with all its contents are now completely gone'
            in message)
        self.assertNotContains(self.get_by_path(''), 'Sub Article 1')

    def test_revision_conflict(self):
        """Test the warning if the same article is beeing edited concurrently."""
        c = self.c
        response = c.post(
            reverse(
                'wiki:edit',
                kwargs={
                    'path': ''}),
            self.example_data)
        self.assertRedirects(response, reverse('wiki:root'))
        response = c.post(
            reverse(
                'wiki:edit',
                kwargs={
                    'path': ''}),
            self.example_data)
        self.assertContains(
            response,
            'While you were editing, someone else changed the revision.')
        #self.dump_db_status('after test_revision_conflict')

    def test_nested_create(self):
        c = self.c
        response = c.post(
            reverse(
                'wiki:create', kwargs={
                    'path': ''}), {
                'title': 'Level 1', 'slug': 'Level1', 'content': 'Content level 1'})
        self.assertRedirects(
            response,
            reverse(
                'wiki:get',
                kwargs={
                    'path': 'level1/'}))
        response = c.post(
            reverse('wiki:create', kwargs={'path': 'Level1/'}),
            {'title': 'test', 'slug': 'Test', 'content': 'Content on level 2'})
        self.assertRedirects(
            response,
            reverse(
                'wiki:get',
                kwargs={
                    'path': 'level1/test/'}))
        response = c.post(
            reverse(
                'wiki:create', kwargs={
                    'path': ''}), {
                'title': 'test', 'slug': 'Test', 'content': 'Other content on level 1'})
        self.assertRedirects(
            response,
            reverse(
                'wiki:get',
                kwargs={
                    'path': 'test/'}))
        self.assertContains(
            self.get_by_path('Test/'),
            'Other content on level 1')
        self.assertContains(
            self.get_by_path('Level1/Test/'),
            'Content')  # on level 2')

    def test_empty_search(self):
        c = self.c
        response = c.get(reverse('wiki:search'), {'q': 'Article'})
        self.assertContains(response, 'Root Article')
        response = c.get(reverse('wiki:search'), {'q': ''})
        self.assertFalse(response.context['articles'])
