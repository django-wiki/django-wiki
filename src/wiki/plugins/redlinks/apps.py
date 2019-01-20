from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RedlinksConfig(AppConfig):
    name = 'wiki.plugins.redlinks'
    verbose_name = _("Wiki red links")
    label = 'wiki_redlinks'
