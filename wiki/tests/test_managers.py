"""
Tests that the custom queryset methods work, this is important
because the pattern of building them is different from Django
1.5 to 1.6 to 1.7 so there will be 3 patterns in play at the
same time.
"""
from __future__ import absolute_import, print_function, unicode_literals

from wiki.models import Article, URLPath
from wiki.plugins.attachments.models import Attachment

from .base import ArticleWebTestBase


class ArticleManagerTests(ArticleWebTestBase):

    def test_queryset_methods_directly_on_manager(self):

        self.assertEqual(
            Article.objects.can_read(self.superuser1).count(), 1
        )
        self.assertEqual(
            Article.objects.can_write(self.superuser1).count(), 1
        )
        self.assertEqual(Article.objects.active().count(), 1)

    def test_queryset_methods_on_querysets(self):

        self.assertEqual(
            Article.objects.all().can_read(self.superuser1).count(), 1
        )
        self.assertEqual(
            Article.objects.all().can_write(self.superuser1).count(), 1
        )
        self.assertEqual(Article.objects.all().active().count(), 1)

    # See: https://code.djangoproject.com/ticket/22817
    def test_queryset_empty_querysets(self):

        self.assertEqual(
            Article.objects.none().can_read(self.superuser1).count(), 0
        )
        self.assertEqual(
            Article.objects.none().can_write(self.superuser1).count(), 0
        )
        self.assertEqual(Article.objects.none().active().count(), 0)


class AttachmentManagerTests(ArticleWebTestBase):

    def test_queryset_methods_directly_on_manager(self):

        # Do the same for Attachment which uses ArtickeFkManager
        self.assertEqual(
            Attachment.objects.can_read(self.superuser1).count(), 0
        )
        self.assertEqual(
            Attachment.objects.can_write(self.superuser1).count(), 0
        )
        self.assertEqual(Attachment.objects.active().count(), 0)

    def test_queryset_methods_on_querysets(self):

        self.assertEqual(
            Attachment.objects.all().can_read(self.superuser1).count(), 0
        )
        self.assertEqual(
            Attachment.objects.all().can_write(self.superuser1).count(), 0
        )
        self.assertEqual(Attachment.objects.all().active().count(), 0)

    # See: https://code.djangoproject.com/ticket/22817
    def test_queryset_empty_query_sets(self):

        self.assertEqual(
            Attachment.objects.none().can_read(self.superuser1).count(), 0
        )
        self.assertEqual(
            Attachment.objects.none().can_write(self.superuser1).count(), 0
        )
        self.assertEqual(Attachment.objects.none().active().count(), 0)


class URLPathManagerTests(ArticleWebTestBase):

    def test_related_manager_works_with_filters(self):
        root = URLPath.root()
        self.assertNotIn(root.id, [p.id for p in root.children.active()])
