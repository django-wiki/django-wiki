from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PyMdownConfig(AppConfig):
    name = "wiki.plugins.pymdown"
    verbose_name = _("PyMDown Extension")
    label = "wiki_pymdown"
