# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import markdown
from django.core.urlresolvers import reverse_lazy
from django.test import TestCase
from wiki.models import URLPath
from wiki.plugins.links.mdx.djangowikilinks import WikiPathExtension


class WikiPathExtensionTests(TestCase):
    def test_works_with_lazy_functions(self):
        URLPath.create_root()
        config = (
            ('base_url', reverse_lazy('wiki:get', kwargs={'path': ''})),
        )
        md = markdown.Markdown(
            extensions=['extra', WikiPathExtension(config)]
        )
        text = '[Français](wiki:/fr)'
        self.assertEqual(
            md.convert(text),
            '<p><a class="wikipath linknotfound" href="/fr">Français</a></p>',
        )
