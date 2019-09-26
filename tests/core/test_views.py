import pprint

from django.http import JsonResponse
from django.shortcuts import resolve_url
from django.utils import translation
from django.utils.html import escape
from django_functest import FuncBaseMixin
from wiki import models
from wiki.forms import validate_slug_numbers
from wiki.models import ArticleRevision, URLPath, reverse

from ..base import ArticleWebTestUtils, DjangoClientTestBase, RequireRootArticleMixin, SeleniumBase, WebTestBase


class RootArticleViewTestsBase(FuncBaseMixin):

    """Tests for creating/viewing the root article."""

    def test_root_article(self):
        """
        Test redirecting to /create-root/,
        creating the root article and a simple markup.
        """
        self.get_url('wiki:root')
        self.assertUrlsEqual(resolve_url('wiki:root_create'))
        self.fill({
            '#id_content': 'test heading h1\n====\n',
            '#id_title': 'Wiki Test',
        })
        self.submit('button[name="save_changes"]')
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

        from wiki.models import Article, ArticleRevision

        for klass in (Article, ArticleRevision, URLPath):
            print('* {} *'.format(klass.__name__))
            pprint.pprint(list(klass.objects.values()), width=240)

    def test_redirects_to_create_if_the_slug_is_unknown(self):

        response = self.get_by_path('unknown/')
        self.assertRedirects(
            response,
            resolve_url('wiki:create', path='') + '?slug=unknown'
        )

    def test_redirects_to_create_with_lowercased_slug(self):

        response = self.get_by_path('Unknown_Linked_Page/')
        self.assertRedirects(
            response,
            resolve_url('wiki:create', path='') + '?slug=unknown_linked_page'
        )

    def test_article_list_update(self):
        """
        Test automatic adding and removing the new article to/from article_list.
        """

        root_data = {
            'content': '[article_list depth:2]',
            'current_revision': str(URLPath.root().article.current_revision.id),
            'preview': '1',
            'title': 'Root Article'
        }

        response = self.client.post(resolve_url('wiki:edit', path=''), root_data)
        self.assertRedirects(response, resolve_url('wiki:root'))

        # verify the new article is added to article_list
        response = self.client.post(
            resolve_url('wiki:create', path=''),
            {'title': 'Sub Article 1', 'slug': 'SubArticle1'}
        )

        self.assertRedirects(
            response,
            resolve_url('wiki:get', path='subarticle1/')
        )
        self.assertContains(self.get_by_path(''), 'Sub Article 1')
        self.assertContains(self.get_by_path(''), 'subarticle1/')

        # verify the deleted article is removed from article_list
        response = self.client.post(
            resolve_url('wiki:delete', path='SubArticle1/'),
            {'confirm': 'on',
             'purge': 'on',
             'revision': str(URLPath.objects.get(slug='subarticle1').article.current_revision.id),
             }
        )

        message = getattr(self.client.cookies['messages'], 'value')

        self.assertRedirects(
            response,
            resolve_url('wiki:get', path='')
        )
        self.assertIn(
            'This article together with all '
            'its contents are now completely gone',
            message)
        self.assertNotContains(self.get_by_path(''), 'Sub Article 1')


class CreateViewTest(RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase):

    def test_create_nested_article_in_article(self):

        response = self.client.post(
            resolve_url('wiki:create', path=''),
            {'title': 'Level 1', 'slug': 'Level1', 'content': 'Content level 1'}
        )
        self.assertRedirects(
            response,
            resolve_url('wiki:get', path='level1/')
        )
        response = self.client.post(
            resolve_url('wiki:create', path='Level1/'),
            {'title': 'test', 'slug': 'Test', 'content': 'Content on level 2'}
        )
        self.assertRedirects(
            response,
            resolve_url('wiki:get', path='level1/test/')
        )
        response = self.client.post(
            resolve_url('wiki:create', path=''),
            {'title': 'test',
             'slug': 'Test',
             'content': 'Other content on level 1'
             }
        )

        self.assertRedirects(
            response,
            resolve_url('wiki:get', path='test/')
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

        # A slug cannot be '123' because it gets confused with an article ID.
        response = self.client.post(
            resolve_url('wiki:create', path=''),
            {'title': 'Illegal slug', 'slug': '123', 'content': 'blah'}
        )
        self.assertContains(
            response,
            escape(validate_slug_numbers.message)
        )


class MoveViewTest(RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase):

    def test_illegal_slug(self):
        # A slug cannot be '123' because it gets confused with an article ID.
        response = self.client.post(
            resolve_url('wiki:move', path=''),
            {'destination': '', 'slug': '123', 'redirect': ''}
        )
        self.assertContains(
            response,
            escape(validate_slug_numbers.message)
        )

    def test_move(self):
        # Create a hierarchy of pages
        self.client.post(
            resolve_url('wiki:create', path=''),
            {'title': 'Test', 'slug': 'test0', 'content': 'Content .0.'}
        )
        self.client.post(
            resolve_url('wiki:create', path='test0/'),
            {'title': 'Test00', 'slug': 'test00', 'content': 'Content .00.'}
        )
        self.client.post(
            resolve_url('wiki:create', path=''),
            {'title': 'Test1', 'slug': 'test1', 'content': 'Content .1.'}
        )
        self.client.post(
            resolve_url('wiki:create', path='test1/'),
            {'title': 'Tes10', 'slug': 'test10', 'content': 'Content .10.'}
        )
        self.client.post(
            resolve_url('wiki:create', path='test1/test10/'),
            {'title': 'Test100', 'slug': 'test100', 'content': 'Content .100.'}
        )

        # Move /test1 => /test0 (an already existing destination slug!)
        response = self.client.post(
            resolve_url('wiki:move', path='test1/'),
            {
                'destination': str(URLPath.root().article.current_revision.id),
                'slug': 'test0',
                'redirect': ''
            }
        )
        self.assertContains(response, 'A slug named')
        self.assertContains(response, 'already exists.')

        # Move /test1 >= /test2 (valid slug), no redirect
        test0_id = URLPath.objects.get(slug='test0').article.current_revision.id
        response = self.client.post(
            resolve_url('wiki:move', path='test1/'),
            {'destination': str(test0_id), 'slug': 'test2', 'redirect': ''}
        )
        self.assertRedirects(
            response,
            resolve_url('wiki:get', path='test0/test2/')
        )

        # Check that there is no article displayed in this path anymore
        response = self.get_by_path('test1/')
        self.assertRedirects(response, '/_create/?slug=test1')

        # Create /test0/test2/test020
        response = self.client.post(
            resolve_url('wiki:create', path='test0/test2/'),
            {'title': 'Test020', 'slug': 'test020', 'content': 'Content .020.'}
        )
        # Move /test0/test2 => /test1new + create redirect
        response = self.client.post(
            resolve_url('wiki:move', path='test0/test2/'),
            {
                'destination': str(URLPath.root().article.current_revision.id),
                'slug': 'test1new', 'redirect': 'true'
            }
        )
        self.assertRedirects(
            response,
            resolve_url('wiki:get', path='test1new/')
        )

        # Check that /test1new is a valid path
        response = self.get_by_path('test1new/')
        self.assertContains(response, 'Content .1.')

        # Check that the child article test0/test2/test020 was also moved
        response = self.get_by_path('test1new/test020/')
        self.assertContains(response, 'Content .020.')

        response = self.get_by_path('test0/test2/')
        self.assertContains(response, 'Moved: Test1')
        self.assertRegex(response.rendered_content, r'moved to <a[^>]*>wiki:/test1new/')

        response = self.get_by_path('test0/test2/test020/')
        self.assertContains(response, 'Moved: Test020')
        self.assertRegex(response.rendered_content, r'moved to <a[^>]*>wiki:/test1new/test020')

        # Check that moved_to was correctly set
        urlsrc = URLPath.get_by_path('/test0/test2/')
        urldst = URLPath.get_by_path('/test1new/')
        self.assertEqual(urlsrc.moved_to, urldst)

        # Check that moved_to was correctly set on the child's previous path
        urlsrc = URLPath.get_by_path('/test0/test2/test020/')
        urldst = URLPath.get_by_path('/test1new/test020/')
        self.assertEqual(urlsrc.moved_to, urldst)

    def test_translation(self):
        # Test that translation of "Be careful, links to this article" exists.
        self.client.post(
            resolve_url('wiki:create', path=''),
            {'title': 'Test', 'slug': 'test0', 'content': 'Content'}
        )
        url = resolve_url('wiki:move', path='test0/')
        response_en = self.client.get(url)
        self.assertIn('Move article', response_en.rendered_content)
        self.assertIn('Be careful', response_en.rendered_content)

        with translation.override('da-DK'):
            response_da = self.client.get(url)

            self.assertNotIn('Move article', response_da.rendered_content)
            self.assertNotIn('Be careful', response_da.rendered_content)


class DeleteViewTest(RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase):

    def test_articles_cache_is_cleared_after_deleting(self):

        # That bug is tested by one individual test, otherwise it could be
        # revealed only by sequence of tests in some particular order

        response = self.client.post(
            resolve_url('wiki:create', path=''),
            {'title': 'Test cache', 'slug': 'testcache', 'content': 'Content 1'}
        )

        self.assertRedirects(
            response,
            resolve_url('wiki:get', path='testcache/')
        )

        response = self.client.post(
            resolve_url('wiki:delete', path='testcache/'),
            {'confirm': 'on', 'purge': 'on',
             'revision': str(URLPath.objects.get(slug='testcache').article.current_revision.id)}
        )

        self.assertRedirects(
            response,
            resolve_url('wiki:get', path='')
        )
        response = self.client.post(
            resolve_url('wiki:create', path=''),
            {'title': 'Test cache', 'slug': 'TestCache', 'content': 'Content 2'}
        )

        self.assertRedirects(
            response,
            resolve_url('wiki:get', path='testcache/')
        )
        # test the cache
        self.assertContains(self.get_by_path('TestCache/'), 'Content 2')


class EditViewTest(RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase):

    def test_preview_save(self):
        """Test edit preview, edit save and messages."""

        example_data = {
            'content': 'The modified text',
            'current_revision': str(URLPath.root().article.current_revision.id),
            'preview': '1',
            # 'save': '1',  # probably not too important
            'summary': 'why edited',
            'title': 'wiki test'
        }

        # test preview
        response = self.client.post(
            resolve_url('wiki:preview', path=''),  # url: '/_preview/'
            example_data
        )

        self.assertContains(response, 'The modified text')

    def test_preview_xframe_options_sameorigin(self):
        """Ensure that preview response has X-Frame-Options: SAMEORIGIN"""

        example_data = {
            'content': 'The modified text',
            'current_revision': str(URLPath.root().article.current_revision.id),
            'preview': '1',
            'summary': 'why edited',
            'title': 'wiki test'
        }

        response = self.client.post(
            resolve_url('wiki:preview', path=''),
            example_data
        )

        self.assertEquals(response.get('X-Frame-Options'), 'SAMEORIGIN')

    def test_revision_conflict(self):
        """
        Test the warning if the same article is being edited concurrently.
        """

        example_data = {
            'content': 'More modifications',
            'current_revision': str(URLPath.root().article.current_revision.id),
            'preview': '0',
            'save': '1',
            'summary': 'why edited',
            'title': 'wiki test'
        }

        response = self.client.post(
            resolve_url('wiki:edit', path=''),
            example_data
        )

        self.assertRedirects(response, resolve_url('wiki:root'))

        response = self.client.post(
            resolve_url('wiki:edit', path=''),
            example_data
        )

        self.assertContains(
            response,
            'While you were editing, someone else changed the revision.'
        )


class DiffViewTests(RequireRootArticleMixin, DjangoClientTestBase):

    def setUp(self):
        super().setUp()
        self.root_article.add_revision(ArticleRevision(
            title='New Revision'), save=True
        )
        self.new_revision = self.root_article.current_revision

    def test_diff(self):
        response = self.client.get(reverse('wiki:diff', kwargs={'revision_id': self.root_article.pk}))
        diff = {
            "diff": ["+ root article content"],
            "other_changes": [["New title", "Root Article"]]
        }
        self.assertJSONEqual(str(response.content, encoding='utf8'), diff)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)


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

    # Javascript only tests:
    def test_preview_and_save(self):
        self.get_url('wiki:edit', path='')
        self.fill({
            '#id_content': 'Some changed stuff',
            '#id_summary': 'why edited',
            '#id_title': 'wiki test'
        })
        self.click('#id_preview')
        self.submit('#id_preview_save_changes')
        new_revision = URLPath.root().article.current_revision
        self.assertIn("Some changed stuff", new_revision.content)


class SearchViewTest(RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase):

    def test_query_string(self):

        response = self.client.get(resolve_url('wiki:search'), {'q': 'Article'})
        self.assertContains(response, 'Root Article')

    def test_empty_query_string(self):

        response = self.client.get(resolve_url('wiki:search'), {'q': ''})
        self.assertFalse(response.context['articles'])

    def test_hierarchy_search(self):

        c = self.client

        c.post(
            resolve_url('wiki:create', path=''),
            {'title': 'Test0', 'slug': 'test0', 'content': 'Content test0'}
        )
        c.post(
            resolve_url('wiki:create', path=''),
            {'title': 'Test1', 'slug': 'test1', 'content': 'Content test1'}
        )
        c.post(
            resolve_url('wiki:create', path='test0/'),
            {'title': 'Subtest0', 'slug': 'subtest0', 'content': 'Content test2'}
        )

        response = c.get(resolve_url('wiki:search', path='test0/'), {'q': 'Content test'})
        articles = response.context['articles']

        def contains_title(articles, title):
            return any(article.current_revision.title == title for article in articles)

        self.assertIs(contains_title(articles, 'Test0'), True)
        self.assertIs(contains_title(articles, 'Test1'), False)
        self.assertIs(contains_title(articles, 'Subtest0'), True)

    def test_hierarchy_search_404(self):

        c = self.client

        response = c.get(resolve_url(
            'wiki:search', path='test0/'), {'q': 'Content test'})

        self.assertEqual(response.status_code, 404)


class DeletedListViewTest(RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase):

    def test_deleted_articles_list(self):
        response = self.client.post(
            resolve_url('wiki:create', path=''),
            {'title': 'Delete Me', 'slug': 'deleteme', 'content': 'delete me please!'}
        )

        self.assertRedirects(
            response,
            resolve_url('wiki:get', path='deleteme/')
        )

        response = self.client.post(
            resolve_url('wiki:delete', path='deleteme/'),
            {'confirm': 'on',
             'revision': URLPath.objects.get(slug='deleteme').article.current_revision.id}
        )

        self.assertRedirects(
            response,
            resolve_url('wiki:get', path='')
        )

        response = self.client.get(resolve_url('wiki:deleted_list'))
        self.assertContains(response, 'Delete Me')


class MergeViewTest(RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase):

    def test_merge_preview(self):
        """Test merge preview"""

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
        self.client.post(
            resolve_url('wiki:edit', path=''),
            example_data
        )

        new_revision = models.Article.objects.get(
            id=self.root_article.id
        ).current_revision

        response = self.client.get(
            resolve_url(
                'wiki:merge_revision_preview',
                article_id=self.root_article.id, revision_id=first_revision.id
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
