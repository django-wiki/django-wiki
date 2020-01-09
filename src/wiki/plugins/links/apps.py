from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LinksConfig(AppConfig):
    name = "wiki.plugins.links"
    verbose_name = _("Wiki links")
    label = "wiki_links"
