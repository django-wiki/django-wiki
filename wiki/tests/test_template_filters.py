from __future__ import absolute_import
from __future__ import unicode_literals

from django.contrib.auth import get_user_model

from wiki.models import Article, ArticleRevision
from wiki.tests.base import wiki_override_settings, BaseTestCase
from wiki.templatetags.wiki_tags import (
    get_content_snippet,
    can_read,
    can_write,
    can_delete,
    can_moderate,
    is_locked
)


class GetContentSnippet(BaseTestCase):

    pass


class CanRead(BaseTestCase):

    template = """
        {% load wiki_tags %}
        {{ article|can_read:user }}
    """

    @wiki_override_settings(WIKI_CAN_READ=lambda *args: True)
    def test_user_have_permission(self):

        a = Article.objects.create()

        User = get_user_model()
        u = User.objects.create(username='Nobody', password='pass')

        output = can_read(a, u)
        self.assertTrue(output)

        output = self.render(self.template, {'article': a, 'user': u})
        self.assertIn('True', output)

    @wiki_override_settings(WIKI_CAN_READ=lambda *args: False)
    def test_user_dont_have_permission(self):

        User = get_user_model()

        a = Article.objects.create()
        u = User.objects.create(username='Noman', password='pass')

        output = can_read(a, u)
        self.assertFalse(output)

        output = self.render(self.template, {'article': a, 'user': u})
        self.assertIn('False', output)


class CanWrite(BaseTestCase):

    template = """
        {% load wiki_tags %}
        {{ article|can_write:user }}
    """

    @wiki_override_settings(WIKI_CAN_DELETE=lambda *args: True)
    def test_user_have_permission(self):

        a = Article.objects.create()

        User = get_user_model()
        u = User.objects.create(username='Nobody', password='pass')

        output = can_write(a, u)
        self.assertTrue(output)

        output = self.render(self.template, {'article': a, 'user': u})
        self.assertIn('True', output)

    @wiki_override_settings(WIKI_CAN_WRITE=lambda *args: False)
    def test_user_dont_have_permission(self):

        User = get_user_model()

        a = Article.objects.create()
        u = User.objects.create(username='Noman', password='pass')

        output = can_write(a, u)
        self.assertFalse(output)

        output = self.render(self.template, {'article': a, 'user': u})
        self.assertIn('False', output)


class CanDelete(BaseTestCase):

    template = """
        {% load wiki_tags %}
        {{ article|can_delete:user }}
    """

    @wiki_override_settings(WIKI_CAN_DELETE=lambda *args: True)
    def test_user_have_permission(self):

        a = Article.objects.create()

        User = get_user_model()
        u = User.objects.create(username='Nobody', password='pass')

        output = can_delete(a, u)
        self.assertTrue(output)

        output = self.render(self.template, {'article': a, 'user': u})
        self.assertIn('True', output)

    @wiki_override_settings(WIKI_CAN_WRITE=lambda *args: False)
    def test_user_dont_have_permission(self):

        User = get_user_model()

        a = Article.objects.create()
        u = User.objects.create(username='Noman', password='pass')

        output = can_delete(a, u)
        self.assertFalse(output)

        output = self.render(self.template, {'article': a, 'user': u})
        self.assertIn('False', output)


class CanModerate(BaseTestCase):

    template = """
        {% load wiki_tags %}
        {{ article|can_moderate:user }}
    """

    @wiki_override_settings(WIKI_CAN_MODERATE=lambda *args: True)
    def test_user_have_permission(self):

        a = Article.objects.create()

        User = get_user_model()
        u = User.objects.create(username='Nobody', password='pass')

        output = can_moderate(a, u)
        self.assertTrue(output)

        output = self.render(self.template, {'article': a, 'user': u})
        self.assertIn('True', output)

    def test_user_dont_have_permission(self):

        User = get_user_model()

        a = Article.objects.create()
        u = User.objects.create(username='Noman', password='pass')

        output = can_moderate(a, u)
        self.assertFalse(output)

        output = self.render(self.template, {'article': a, 'user': u})
        self.assertIn('False', output)


class IsLocked(BaseTestCase):

    template = """
        {% load wiki_tags %}
        {{ article|is_locked }}
    """

    def test_no_current_revision(self):

        a = Article.objects.create()

        output = is_locked(a)
        self.assertFalse(output)

        output = self.render(self.template, {'article': a})
        self.assertIn('None', output)

    def test_have_current_revision_and_not_locked(self):

        a = Article.objects.create()
        ArticleRevision.objects.create(article=a, locked=False)

        b = Article.objects.create()
        ArticleRevision.objects.create(article=b)

        output = is_locked(a)
        self.assertFalse(output)

        output = is_locked(b)
        self.assertFalse(output)

        output = self.render(self.template, {'article': a})
        self.assertIn('False', output)

    def test_have_current_revision_and_locked(self):

        a = Article.objects.create()
        ArticleRevision.objects.create(article=a, locked=True)

        output = is_locked(a)
        self.assertTrue(output)

        output = self.render(self.template, {'article': a})
        self.assertIn('True', output)
