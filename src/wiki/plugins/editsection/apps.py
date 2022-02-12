from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EditSectionConfig(AppConfig):
    name = "wiki.plugins.editsection"
    verbose_name = _("Wiki edit section")
    label = "wiki_editsection"
