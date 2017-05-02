from __future__ import absolute_import, print_function, unicode_literals

import pprint

from django.contrib.auth import authenticate
from django.utils.html import escape
from django_functest import FuncBaseMixin
from wiki import models
from wiki.forms import validate_slug_numbers
from wiki.models import reverse, URLPath

from ..base import RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase, SeleniumBase, WebTestBase


class RootArticleViewTestsBase(FuncBaseMixin):

    """Tests for creating/viewing the root article."""

    def test_root_article(self):
        """
        Test redirecting to /create-root/,
        creating the root article and a simple markup.
        """
        self.get_url('wiki:root')
        self.assertUrlsEqual(reverse('wiki:root_create'))
        self.fill({
            '#id_content': 'test heading h1\n====\n',
            '#id_title': 'Wiki Test',
        })
        self.submit('input[name="save_changes"]')
        self.assertUrlsEqual('/')
        self.assertTextPresent('test heading h1')
        article = URLPath.root().article
        self.assertIn('test heading h1', article.current_revision.content)


class RootArticleViewTestsWebTest(RootArticleViewTestsBase, WebTestBase):
    pass


class RootArticleViewTestsSelenium(RootArticleViewTestsBase, SeleniumBase):
    pass


class ArticleViewViewTests(RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase):

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

    def test_redirects_to_create_if_the_slug_is_unknown(self):

        response = self.get_by_path('unknown/')
        self.assertRedirects(
            response,
            reverse('wiki:create', kwargs={'path': ''}) + '?slug=unknown'
        )

    def test_redirects_to_create_with_lowercased_slug(self):

        response = self.get_by_path('Unknown_Linked_Page/')
        self.assertRedirects(
            response,
            reverse('wiki:create', kwargs={'path': ''}) + '?slug=unknown_linked_page'
        )

    def test_article_list_update(self):
        """
        Test automatic adding and removing the new article to/from article_list.
        """

        c = self.c
        root_data = {
            'content': '[article_list depth:2]',
            'current_revision': str(URLPath.root().article.current_revision.id),
            'preview': '1',
            'title': 'Root Article'
        }

        response = c.post(reverse('wiki:edit', kwargs={'path': ''}), root_data)
        self.assertRedirects(response, reverse('wiki:root'))

        # verify the new article is added to article_list
        response = c.post(
            reverse('wiki:create', kwargs={'path': ''}),
            {'title': 'Sub Article 1', 'slug': 'SubArticle1'}
        )

        self.assertRedirects(
            response,
            reverse('wiki:get', kwargs={'path': 'subarticle1/'})
        )
        self.assertContains(self.get_by_path(''), 'Sub Article 1')
        self.assertContains(self.get_by_path(''), 'subarticle1/')

        # verify the deleted article is removed from article_list
        response = c.post(
            reverse('wiki:delete', kwargs={'path': 'SubArticle1/'}),
            {'confirm': 'on',
             'purge': 'on',
             'revision': str(URLPath.objects.get(slug='subarticle1').article.current_revision.id),
             }
        )

        message = getattr(c.cookies['messages'], 'value')

        self.assertRedirects(
            response,
            reverse('wiki:get', kwargs={'path': ''})
        )
        self.assertIn(
            'This article together with all '
            'its contents are now completely gone',
            message)
        self.assertNotContains(self.get_by_path(''), 'Sub Article 1')


class CreateViewTest(RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase):

    def test_create_nested_article_in_article(self):

        c = self.c

        response = c.post(
            reverse('wiki:create', kwargs={'path': ''}),
            {'title': 'Level 1', 'slug': 'Level1', 'content': 'Content level 1'}
        )
        self.assertRedirects(
            response,
            reverse('wiki:get', kwargs={'path': 'level1/'})
        )
        response = c.post(
            reverse('wiki:create', kwargs={'path': 'Level1/'}),
            {'title': 'test', 'slug': 'Test', 'content': 'Content on level 2'}
        )
        self.assertRedirects(
            response,
            reverse('wiki:get', kwargs={'path': 'level1/test/'})
        )
        response = c.post(
            reverse('wiki:create', kwargs={'path': ''}),
            {'title': 'test',
             'slug': 'Test',
             'content': 'Other content on level 1'
             }
        )

        self.assertRedirects(
            response,
            reverse('wiki:get', kwargs={'path': 'test/'})
        )
        self.assertContains(
            self.get_by_path('Test/'),
            'Other content on level 1'
        )
        self.assertContains(
            self.get_by_path('Level1/Test/'),
            'Content'
        )  # on level 2')

    def test_illegal_slug(self):

        c = self.c

        # A slug cannot be '123' because it gets confused with an article ID.
        response = c.post(
            reverse('wiki:create', kwargs={'path': ''}),
            {'title': 'Illegal slug', 'slug': '123', 'content': 'blah'}
        )
        self.assertContains(
            response,
            escape(validate_slug_numbers.message)
        )



class DeleteViewTest(RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase):

    def test_articles_cache_is_cleared_after_deleting(self):

        # That bug is tested by one individual test, otherwise it could be
        # revealed only by sequence of tests in some particular order
        c = self.c

        response = c.post(
            reverse('wiki:create', kwargs={'path': ''}),
            {'title': 'Test cache', 'slug': 'testcache', 'content': 'Content 1'}
        )

        self.assertRedirects(
            response,
            reverse('wiki:get', kwargs={'path': 'testcache/'})
        )

        response = c.post(
            reverse('wiki:delete', kwargs={'path': 'testcache/'}),
            {'confirm': 'on', 'purge': 'on',
             'revision': str(URLPath.objects.get(slug='testcache').article.current_revision.id)}
        )

        self.assertRedirects(
            response,
            reverse('wiki:get', kwargs={'path': ''})
        )
        response = c.post(
            reverse('wiki:create', kwargs={'path': ''}),
            {'title': 'Test cache', 'slug': 'TestCache', 'content': 'Content 2'}
        )

        self.assertRedirects(
            response,
            reverse('wiki:get', kwargs={'path': 'testcache/'})
        )
        # test the cache
        self.assertContains(self.get_by_path('TestCache/'), 'Content 2')


class EditViewTest(RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase):

    def test_preview_save(self):
        """Test edit preview, edit save and messages."""

        c = self.c
        example_data = {
            'content': 'The modified text',
            'current_revision': str(URLPath.root().article.current_revision.id),
            'preview': '1',
            # 'save': '1',  # probably not too important
            'summary': 'why edited',
            'title': 'wiki test'
        }

        # test preview
        response = c.post(
            reverse('wiki:preview', kwargs={'path': ''}),  # url: '/_preview/'
            example_data
        )

        self.assertContains(response, 'The modified text')

    def test_revision_conflict(self):
        """
        Test the warning if the same article is being edited concurrently.
        """

        c = self.c

        example_data = {
            'content': 'More modifications',
            'current_revision': str(URLPath.root().article.current_revision.id),
            'preview': '0',
            'save': '1',
            'summary': 'why edited',
            'title': 'wiki test'
        }

        response = c.post(
            reverse('wiki:edit', kwargs={'path': ''}),
            example_data
        )

        self.assertRedirects(response, reverse('wiki:root'))

        response = c.post(
            reverse('wiki:edit', kwargs={'path': ''}),
            example_data
        )

        self.assertContains(
            response,
            'While you were editing, someone else changed the revision.'
        )

class EditViewTestsBase(RequireRootArticleMixin, FuncBaseMixin):
    def test_edit_save(self):
        old_revision = URLPath.root().article.current_revision
        self.get_url('wiki:edit', path='')
        self.fill({
            '#id_content': 'Something 2',
            '#id_summary': 'why edited',
            '#id_title': 'wiki test'
        })
        self.submit('#id_save')
        self.assertTextPresent('Something 2')
        self.assertTextPresent('successfully added')
        new_revision = URLPath.root().article.current_revision
        self.assertIn('Something 2', new_revision.content)
        self.assertEqual(new_revision.revision_number, old_revision.revision_number + 1)


class EditViewTestsWebTest(EditViewTestsBase, WebTestBase):
    pass


class EditViewTestsSelenium(EditViewTestsBase, SeleniumBase):
    pass



class SearchViewTest(RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase):

    def test_query_string(self):

        c = self.c

        response = c.get(reverse('wiki:search'), {'q': 'Article'})
        self.assertContains(response, 'Root Article')

    def test_empty_query_string(self):

        c = self.c

        response = c.get(reverse('wiki:search'), {'q': ''})
        self.assertFalse(response.context['articles'])


class DeletedListViewTest(RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase):

    def test_deleted_articles_list(self):
        c = self.c

        response = c.post(
            reverse('wiki:create', kwargs={'path': ''}),
            {'title': 'Delete Me', 'slug': 'deleteme', 'content': 'delete me please!'}
        )

        self.assertRedirects(
            response,
            reverse('wiki:get', kwargs={'path': 'deleteme/'})
        )

        response = c.post(
            reverse('wiki:delete', kwargs={'path': 'deleteme/'}),
            {'confirm': 'on',
             'revision': URLPath.objects.get(slug='deleteme').article.current_revision.id}
        )

        self.assertRedirects(
            response,
            reverse('wiki:get', kwargs={'path': ''})
        )

        response = c.get(reverse('wiki:deleted_list'))
        self.assertContains(response, 'Delete Me')


class UpdateProfileViewTest(RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase):

    def test_update_profile(self):
        c = self.c

        c.post(
            reverse('wiki:profile_update'),
            {"email": "test@test.com", "password1": "newPass", "password2": "newPass"},
            follow=True
        )

        test_auth = authenticate(username='admin', password='newPass')

        self.assertNotEqual(test_auth, None)
        self.assertEqual(test_auth.email, 'test@test.com')


class MergeViewTest(RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase):

    def test_merge_preview(self):
        """Test merge preview"""

        c = self.c
        first_revision = self.root_article.current_revision
        example_data = {
            'content': 'More modifications\n\nMerge new line',
            'current_revision': str(first_revision.id),
            'preview': '0',
            'save': '1',
            'summary': 'testing merge',
            'title': 'wiki test'
        }


        # save a new revision
        c.post(
            reverse('wiki:edit', kwargs={'path': ''}),
            example_data
        )

        new_revision = models.Article.objects.get(
            id=self.root_article.id
        ).current_revision

        response = c.get(
            reverse(
                'wiki:merge_revision_preview',
                kwargs={'article_id': self.root_article.id, 'revision_id': first_revision.id}
            ),
        )

        self.assertContains(
            response,
            'Previewing merge between:'
        )
        self.assertContains(
            response,
            '#{rev_number}'.format(rev_number=first_revision.revision_number)
        )
        self.assertContains(
            response,
            '#{rev_number}'.format(rev_number=new_revision.revision_number)
        )
