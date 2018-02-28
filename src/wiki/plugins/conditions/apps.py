from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ConditionsConfig(AppConfig):
    name = 'wiki.plugins.conditions'
    verbose_name = _("Conditions")
    label = 'wiki_conditions'
