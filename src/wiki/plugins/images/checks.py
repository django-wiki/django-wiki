from django.apps import apps
from django.core.checks import Error


class Tags:
    required_installed_apps = "required_installed_apps"


def check_for_required_installed_apps(app_configs, **kwargs):
    errors = []
    if not apps.is_installed("sorl.thumbnail"):
        errors.append(
            Error("needs sorl.thumbnail in INSTALLED_APPS", id="wiki_images.E001")
        )
    return errors
