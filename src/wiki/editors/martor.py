# -*- coding: utf-8
from __future__ import absolute_import, unicode_literals

from wiki.editors.base import BaseEditor

from martor.widgets import MartorWidget
from django.conf.urls import include, url
from django.conf import settings

class Martor(BaseEditor):
    editor_id = 'martorId'

    def get_admin_widget(self, instance=None):
        m = MartorWidget()
        return m

    def get_widget(self, instance=None):
        m = MartorWidget()

        if settings.EDITOR_INCLUDE_JAVASCRIPT is False:
            m.Media.js = ()
        return m

    def get_urls(self):
        return [url(r'^martor/', include('martor.urls')), ]

    class AdminMedia:
        css = {
            "wiki/css/editors/martor.css",
        }

        js = ()
        if settings.EDITOR_INCLUDE_JAVASCRIPT is True:
            js = (
                "wiki/js/editors/martor-patch.js",
            )

    class Media:
        css = {
            'all': (
                "wiki/css/editors/martor.css", ),
        }
        js = ()
        if settings.EDITOR_INCLUDE_JAVASCRIPT is True:
            js = (
                "wiki/js/editors/martor-patch.js",
            )
