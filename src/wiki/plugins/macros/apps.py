from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MacrosConfig(AppConfig):
    name = 'wiki.plugins.macros'
    verbose_name = _("Wiki macros")
    label = 'wiki_macros'
