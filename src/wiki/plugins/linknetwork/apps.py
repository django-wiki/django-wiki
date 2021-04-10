from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LinkNetworkConfig(AppConfig):
    name = "wiki.plugins.linknetwork"
    verbose_name = _("Link Network")
    label = "wiki_linknetwork"
