from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model
from wiki.models import Article, ArticleRevision
from wiki.templatetags.wiki_tags import (can_delete, can_moderate, can_read,
                                         can_write, get_content_snippet,
                                         is_locked)
from wiki.tests.base import TemplateTestCase, wiki_override_settings

User = get_user_model()



class GetContentSnippet(TemplateTestCase):

    template = """
        {% load wiki_tags %}
        {{ some_content|get_content_snippet:"keyword, max_words" }}
    """

    def test_keyword_at_the_end_of_the_content(self):
        text = 'lorem ' * 80
        content = text + ' list'
        expected = (
            'lorem lorem lorem lorem lorem lorem lorem lorem lorem '
            'lorem lorem lorem lorem lorem lorem <strong>list</strong> '
        )

        output = get_content_snippet(content, 'list')

        self.assertEqual(output, expected)

    def test_keyword_at_the_beginning_of_the_content(self):
        text = 'lorem ' * 80
        content = 'list ' + text
        expected = (
            ' <strong>list</strong> lorem lorem lorem lorem lorem '
            'lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem '
            'lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem '
            'lorem lorem lorem'
        )

        output = get_content_snippet(content, 'list')

        self.assertEqual(output, expected)

    def test_whole_content_is_consist_from_keywords(self):
        content = 'lorem ' * 80
        expected = (
            '<strong>lorem</strong> <strong>lorem</strong> '
            '<strong>lorem</strong> <strong>lorem</strong> '
            '<strong>lorem</strong> <strong>lorem</strong> '
            '<strong>lorem</strong> <strong>lorem</strong> '
            '<strong>lorem</strong> <strong>lorem</strong> '
            '<strong>lorem</strong> <strong>lorem</strong> '
            '<strong>lorem</strong> <strong>lorem</strong> '
            '<strong>lorem</strong> <strong>lorem</strong> '
        )

        output = get_content_snippet(content, 'lorem')

        self.assertEqual(output, expected)

    def test_keyword_is_not_in_a_content(self):
        content = 'lorem ' * 80
        expected = (
            'lorem lorem lorem lorem lorem lorem lorem lorem lorem '
            'lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem '
            'lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem'
        )

        output = get_content_snippet(content, 'list')

        self.assertEqual(output, expected)

    def test_a_few_keywords_in_content(self):
        text = 'lorem ' * 80
        content = 'list ' + text

        text = 'ipsum ' * 80
        content += text + ' list '

        text = 'dolorum ' * 80
        content += text + ' list'

        expected = (
            'dolorum dolorum dolorum dolorum dolorum dolorum dolorum '
            'dolorum dolorum dolorum dolorum dolorum dolorum dolorum dolorum '
            '<strong>list</strong> '
        )

        output = get_content_snippet(content, 'list')

        self.assertEqual(output, expected)

    # XXX bug or feature?
    def test_keyword_is_in_content_and_max_words_is_zero(self):
        text = 'spam ' * 800
        content = text + ' list'

        output = get_content_snippet(content, 'list', 0)
        expected = 'spam ' * 800 + '<strong>list</strong> '

        self.assertEqual(output, expected)

    # XXX bug or feature?
    def test_keyword_is_in_content_and_max_words_is_negative(self):
        text = 'spam ' * 80
        content = text + ' list'

        output = get_content_snippet(content, 'list', -10)
        expected = 'spam ' * 75 + '<strong>list</strong> '

        self.assertEqual(output, expected)

    # XXX bug or feature?
    def test_keyword_is_not_in_content_and_max_words_is_zero(self):
        content = 'spam ' * 15

        output = get_content_snippet(content, 'list', 0)
        expected = ''

        self.assertEqual(output, expected)

    # XXX bug or feature?
    def test_keyword_is_not_in_content_and_max_words_is_negative(self):
        content = 'spam ' * 15

        output = get_content_snippet(content, 'list', -10)
        expected = 'spam spam spam spam spam'

        self.assertEqual(output, expected)

    def test_no_content(self):
        content = ''

        output = get_content_snippet(content, 'list')

        self.assertEqual(output, '')

        content = ' '

        output = get_content_snippet(content, 'list')

        self.assertEqual(output, '')

    def test_strip_tags(self):

        keyword = 'maybe'

        content = """
        <h1>Some dummy</h1> text. <div>Actually</div> I don't what to write,
        heh. Don't now, <b>maybe</b> I should citate Shakespeare or Byron.
        Or <a>maybe</a> copy paste from <a href="http://python.org">python</a>
        or django documentation. Maybe.
        """

        expected = (
            'I should citate Shakespeare or Byron. '
            'Or <strong>maybe</strong> copy paste from python '
            'or django documentation. <strong>maybe</strong> .'
        )

        output = get_content_snippet(content, keyword, 30)

        self.assertEqual(output, expected)

    def test_max_words_arg(self):

        keyword = 'eggs'

        content = """
        knight eggs spam ham eggs guido python eggs circus
        """
        expected = ('<strong>eggs</strong> guido python '
                    '<strong>eggs</strong> circus')

        output = get_content_snippet(content, keyword, 5)

        self.assertEqual(output, expected)

        output = get_content_snippet(content, keyword, 0)

        expected = (
            'knight <strong>eggs</strong> spam ham '
            '<strong>eggs</strong> guido python <strong>eggs</strong> '
        )
        self.assertEqual(output, expected)


class CanRead(TemplateTestCase):

    template = """
        {% load wiki_tags %}
        {{ article|can_read:user }}
    """

    @wiki_override_settings(WIKI_CAN_READ=lambda *args: True)
    def test_user_have_permission(self):

        a = Article.objects.create()

        u = User.objects.create(username='Nobody', password='pass')

        output = can_read(a, u)
        self.assertTrue(output)

        output = self.render({'article': a, 'user': u})
        self.assertIn('True', output)

    @wiki_override_settings(WIKI_CAN_READ=lambda *args: False)
    def test_user_dont_have_permission(self):

        a = Article.objects.create()
        u = User.objects.create(username='Noman', password='pass')

        output = can_read(a, u)
        self.assertFalse(output)

        output = self.render({'article': a, 'user': u})
        self.assertIn('False', output)


class CanWrite(TemplateTestCase):

    template = """
        {% load wiki_tags %}
        {{ article|can_write:user }}
    """

    @wiki_override_settings(WIKI_CAN_DELETE=lambda *args: True)
    def test_user_have_permission(self):

        a = Article.objects.create()

        u = User.objects.create(username='Nobody', password='pass')

        output = can_write(a, u)
        self.assertTrue(output)

        output = self.render({'article': a, 'user': u})
        self.assertIn('True', output)

    @wiki_override_settings(WIKI_CAN_WRITE=lambda *args: False)
    def test_user_dont_have_permission(self):

        a = Article.objects.create()
        u = User.objects.create(username='Noman', password='pass')

        output = can_write(a, u)
        self.assertFalse(output)

        output = self.render({'article': a, 'user': u})
        self.assertIn('False', output)


class CanDelete(TemplateTestCase):

    template = """
        {% load wiki_tags %}
        {{ article|can_delete:user }}
    """

    @wiki_override_settings(WIKI_CAN_DELETE=lambda *args: True)
    def test_user_have_permission(self):

        a = Article.objects.create()

        u = User.objects.create(username='Nobody', password='pass')

        output = can_delete(a, u)
        self.assertTrue(output)

        output = self.render({'article': a, 'user': u})
        self.assertIn('True', output)

    @wiki_override_settings(WIKI_CAN_WRITE=lambda *args: False)
    def test_user_dont_have_permission(self):

        a = Article.objects.create()
        u = User.objects.create(username='Noman', password='pass')

        output = can_delete(a, u)
        self.assertFalse(output)

        output = self.render({'article': a, 'user': u})
        self.assertIn('False', output)


class CanModerate(TemplateTestCase):

    template = """
        {% load wiki_tags %}
        {{ article|can_moderate:user }}
    """

    @wiki_override_settings(WIKI_CAN_MODERATE=lambda *args: True)
    def test_user_have_permission(self):

        a = Article.objects.create()

        u = User.objects.create(username='Nobody', password='pass')

        output = can_moderate(a, u)
        self.assertTrue(output)

        output = self.render({'article': a, 'user': u})
        self.assertIn('True', output)

    def test_user_dont_have_permission(self):

        a = Article.objects.create()
        u = User.objects.create(username='Noman', password='pass')

        output = can_moderate(a, u)
        self.assertFalse(output)

        output = self.render({'article': a, 'user': u})
        self.assertIn('False', output)


class IsLocked(TemplateTestCase):

    template = """
        {% load wiki_tags %}
        {{ article|is_locked }}
    """

    def test_no_current_revision(self):

        a = Article.objects.create()

        output = is_locked(a)
        self.assertFalse(output)

        output = self.render({'article': a})
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

        output = self.render({'article': a})
        self.assertIn('False', output)

    def test_have_current_revision_and_locked(self):

        a = Article.objects.create()
        ArticleRevision.objects.create(article=a, locked=True)

        output = is_locked(a)
        self.assertTrue(output)

        output = self.render({'article': a})
        self.assertIn('True', output)


class PluginEnabled(TemplateTestCase):

    template = """
        {% load wiki_tags %}
        {% if "wiki.plugins.attachments"|plugin_enabled %}It is enabled{% endif %}
    """

    def test_true(self):
        output = self.render({})
        self.assertIn('It is enabled', output)


class WikiSettings(TemplateTestCase):

    template = """
        {% load wiki_tags %}
        {% if "ACCOUNT_HANDLING"|wiki_settings %}It is enabled{% endif %}
    """

    @wiki_override_settings(WIKI_ACCOUNT_HANDLING=lambda *args: True)
    def test_setting(self):
        output = self.render({})
        self.assertIn('It is enabled', output)
