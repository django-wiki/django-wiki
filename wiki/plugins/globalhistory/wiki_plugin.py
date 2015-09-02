from __future__ import absolute_import
from __future__ import unicode_literals
from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin

from django.conf.urls import url

from . import settings, views


class GlobalHistoryPlugin(BasePlugin):

    slug = settings.SLUG
    urlpatterns = {'root': [
        url(r'^$', views.GlobalHistory.as_view(), name='globalhistory'),
    ]}

    def __init__(self):
        pass

registry.register(GlobalHistoryPlugin)
