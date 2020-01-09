from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GlobalHistoryConfig(AppConfig):
    name = "wiki.plugins.globalhistory"
    verbose_name = _("Wiki Global History")
    label = "wiki_globalhistory"
