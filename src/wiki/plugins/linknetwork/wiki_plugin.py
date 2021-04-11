from django.urls import re_path
from django.utils.translation import gettext as _
from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin

from . import settings
from . import views


class LinkNetworkPlugin(BasePlugin):
    slug = settings.SLUG

    # TODO: By default, show the 'what links here', which in turn should link to the network.
    article_tab = (_("What links here"), "fa fa-sitemap")

    urlpatterns = {
        "root": [
            re_path(
                r"^update/$", views.GlobalUpdate.as_view(), name="linknetwork-update"
            ),
        ],
        "article": [
            re_path(r"^$", views.LinkNetwork.as_view(), name="linknetwork"),
            re_path(
                r"^whatlinkshere/$", views.WhatLinksHere.as_view(), name="whatlinkshere"
            ),
        ],
    }


registry.register(LinkNetworkPlugin)
