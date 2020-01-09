from django.apps import AppConfig
from django.core.checks import register
from django.utils.translation import gettext_lazy as _

from . import checks


class ImagesConfig(AppConfig):
    name = "wiki.plugins.images"
    verbose_name = _("Wiki images")
    label = "wiki_images"

    def ready(self):
        register(
            checks.check_for_required_installed_apps,
            checks.Tags.required_installed_apps,
        )
