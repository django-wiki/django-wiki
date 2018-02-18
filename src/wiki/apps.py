from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WikiConfig(AppConfig):
    name = "wiki"
    verbose_name = _("Wiki")
