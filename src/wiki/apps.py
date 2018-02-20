from django.apps import AppConfig
from django.core.checks import register
from django.utils.translation import gettext_lazy as _

from . import checks


class WikiConfig(AppConfig):
    name = "wiki"
    verbose_name = _("Wiki")

    def ready(self):
        register(checks.check_for_required_installed_apps, checks.Tags.required_installed_apps)
        register(checks.check_for_obsolete_installed_apps, checks.Tags.obsolete_installed_apps)
        register(checks.check_for_context_processors, checks.Tags.context_processors)
