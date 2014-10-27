from __future__ import print_function
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client


class TemplateTest(TestCase):

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
        c.post(reverse('wiki:root_create'),
            {
               'content': 'root article content\n### Title {{color|blue}}',
               'title': 'Root Article'
            }
        )
        self.example_template_color = {
            "template_title": "color",
            "template_content": "{: style='color:{{{0}}};'}",
            "description": "color style",
        }

    def tearDown(self):
        from wiki.models import Article
        from wiki.plugins.template.models import Template
        Template.objects.all().delete()
        for article in Article.objects.all():
            article.clear_cache()

    def get_by_path(self, path):
        """Get the article response for the path.
           Example:  self.get_by_path("Level1/Slug2/").title
        """
        return self.c.get(reverse('wiki:get', kwargs={'path': path}))

    def test_create_template(self):
        c = self.c
        response = c.post(
            reverse('wiki:template_create', kwargs={'path': ''}),
            self.example_template_color
        )
        self.assertRedirects(
            response,
            reverse('wiki:template_index', kwargs={'path': ''})
        )
        response = c.get(reverse('wiki:template_index', kwargs={'path': ''}))
        self.assertContains(
            response,
            '&#123;&#123;color&#125;&#125;'
        )
        self.assertContains(
            self.get_by_path(''),
            'style="color:blue;"'
        )

    def test_embed_template(self):
        c = self.c
        c.post(
            reverse('wiki:create', kwargs={'path': ''}),
            {
                'title': 'Test cache',
                'slug': 'testcache',
                'content': 'Content 1\n{{glogo}}'
            }
        )
        c.post(
            reverse('wiki:template_create', kwargs={'path': 'testcache/'}),
            {
                "template_title": "glogo",
                "template_content": "![img](http://www.gstatic.com/"
                                    "translate/intl/zh-CN/logo2.png)",
                "description": "google logo",
            }
        )
        self.assertContains(
            self.get_by_path('testcache/'),
            'src="http://www.gstatic.com/translate/intl/zh-CN/logo2.png"'
        )

    def test_change_template(self):
        example_template_color2 = {
            "template_content": "{: style='background-color:{{{0}}};'}",
            "description": "",
        }
        c = self.c
        c.post(
            reverse('wiki:template_create', kwargs={'path': ''}),
            self.example_template_color
        )
        c.post(
            reverse(
                'wiki:template_add_revision',
                kwargs={'path': '', 'template_id': '1'}
            ),
            example_template_color2
        )
        self.assertContains(
            self.get_by_path(''),
            'style="background-color:blue;"'
        )

    def test_template_delete(self):
        # from wiki.models import Article
        c = self.c
        c.post(
            reverse('wiki:template_create', kwargs={'path': ''}),
            self.example_template_color
        )
        self.assertContains(
            self.get_by_path(''),
            'style="color:blue;"'
        )
        response = c.post(
            reverse(
                'wiki:template_delete',
                kwargs={'path': '', 'template_id': '1'}
            ),
            {'confirm': 'on', 'purge': 'on', 'revision': '2'}
        )
        self.assertRedirects(
            response,
            reverse('wiki:template_index', kwargs={'path': ''})
        )
        self.assertContains(
            self.get_by_path(''),
            '{{color|blue}}'
        )
