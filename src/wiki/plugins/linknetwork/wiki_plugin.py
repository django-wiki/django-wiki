from django.urls import re_path
from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin

from . import settings
from . import views


class LinkNetworkPlugin(BasePlugin):
    slug = settings.SLUG

    urlpatterns = {
        "article": [
            re_path(r"^$", views.LinkNetwork.as_view(), name="linknetwork"),
            re_path(
                r"^whatlinkshere/$", views.WhatLinksHere.as_view(), name="whatlinkshere"
            ),
        ]
    }


registry.register(LinkNetworkPlugin)
