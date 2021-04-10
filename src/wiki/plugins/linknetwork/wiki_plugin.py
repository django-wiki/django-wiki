from django.urls import re_path
from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin

from . import settings
from . import views


class LinkNetworkPlugin(BasePlugin):
    slug = settings.NW_SLUG

    urlpatterns = {
        "article": [
            re_path(r"^$", views.LinkNetwork.as_view(), name="linknetwork"),
        ]
    }


class WhatLinksHerePlugin(BasePlugin):
    slug = settings.SLUG

    urlpatterns = {
        "article": [
            re_path(r"^$", views.WhatLinksHere.as_view(), name="whatlinkshere"),
        ]
    }


registry.register(LinkNetworkPlugin)
registry.register(WhatLinksHerePlugin)
