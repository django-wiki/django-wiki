# -*- coding: utf-8
from __future__ import absolute_import, unicode_literals

from wiki.editors.base import BaseEditor

from martor.widgets import MartorWidget
from django.conf.urls import include, url


class Martor(BaseEditor):
    editor_id = 'martorId'

    def get_admin_widget(self, instance=None):
        m = MartorWidget()
        return m

    def get_widget(self, instance=None):
        m = MartorWidget()
        m.Media.css={'all': ()}
        m.Media.js=(
            'plugins/js/ace.js',
            # 'plugins/js/semantic.min.js',
            'plugins/js/mode-markdown.js',
            'plugins/js/ext-language_tools.js',
            'plugins/js/theme-github.js',
            'plugins/js/highlight.min.js',
            'plugins/js/resizable.min.js',
            'plugins/js/emojis.min.js',
            'martor/js/martor.min.js',
        )
        return m

    def get_urls(self):
        return [url(r'^martor/', include('martor.urls')),]

    class AdminMedia:
        css = {
              "wiki/css/editors/martor.css",
        }
        js = (
              "wiki/js/editors/martor.js",
        )

    class Media:
        css = {
            'all': (
              "wiki/css/editors/martor.css",),
        }
        js = (
              "wiki/js/editors/martor.js",
        )
