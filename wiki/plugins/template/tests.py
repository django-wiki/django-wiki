from __future__ import print_function
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from wiki.tests.base import ArticleTestBase


class TemplateTest(ArticleTestBase):

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

    def test_create_template(self):
        self.assertRedirects(
            self.c.post(
                reverse('wiki:template_create', kwargs={'path': ''}),
                self.example_template_color
            ),
            reverse('wiki:template_index', kwargs={'path': ''}),
        )
        self.assertContains(
            self.c.get(reverse('wiki:template_index', kwargs={'path': ''})),
            '&#123;&#123;color&#125;&#125;',
        )

    def test_embed_template(self):
        self.c.post(
            reverse('wiki:create', kwargs={'path': ''}),
            {
                'title': 'Test cache',
                'slug': 'testcache',
                'content': 'Content 1\n{{glogo}}'
            }
        )
        self.c.post(
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

    def test_embed_named_template(self):
        example_template_named_color = {
            "template_title": "named_color",
            "template_content": "{: style='color:{{{color}}};font-size:{{{fontsize}}};'}",
            "description": "named color style",
        }
        self.c.post(
            reverse('wiki:create', kwargs={'path': ''}),
            {
                'title': 'Test named template',
                'slug': 'testnamedtemplate',
                'content': 'Content 1\n{{named_color|color=red|fontsize=12px}}'
            }
        )
        self.c.post(
            reverse('wiki:template_create', kwargs={'path': 'testnamedtemplate/'}),
            example_template_named_color
        )
        self.assertContains(
            self.get_by_path('testnamedtemplate/'),
            'style="color:red;font-size:12px;"'
        )

    def test_change_template(self):
        example_template_color2 = {
            "template_content": "{: style='background-color:{{{0}}};'}",
            "description": "",
        }
        self.c.post(
            reverse('wiki:template_create', kwargs={'path': ''}),
            self.example_template_color
        )
        self.c.post(
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
        self.c.post(
            reverse('wiki:template_create', kwargs={'path': ''}),
            self.example_template_color
        )
        self.assertContains(
            self.get_by_path(''),
            'style="color:blue;"'
        )
        self.assertRedirects(
            self.c.post(
                reverse(
                    'wiki:template_delete',
                    kwargs={'path': '', 'template_id': '1'}
                ),
                {'confirm': 'on', 'purge': 'on', 'revision': '2'}
            ),
            reverse('wiki:template_index', kwargs={'path': ''}),
        )
        self.assertContains(
            self.get_by_path(''),
            '{{color|blue}}'
        )
