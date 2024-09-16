from django.apps import apps
from django.core.checks import Error


class Tags:
    required_installed_apps = "required_installed_apps"


def pillow_installed():
    try:
        import PIL
        pil_version = PIL.__version__
    except Exception as e:
        print(e)
        return False

    return True


def check_for_required_installed_apps(app_configs, **kwargs):
    errors = []

    if not pillow_installed():
        errors.append(
            Error(
                "Pillow is not installed. see https://github.com/django-wiki/django-wiki/blob/main/docs/installation.rst#pre-requisite-pillow", id="wiki_images.E002"
            )
        )

    if not apps.is_installed("sorl.thumbnail"):
        errors.append(
            Error(
                "needs sorl.thumbnail in INSTALLED_APPS", id="wiki_images.E001"
            )
        )
    return errors
