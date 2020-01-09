from django.apps import apps
from django.core.checks import Error
from django.template import Engine


class Tags:
    required_installed_apps = "required_installed_apps"
    obsolete_installed_apps = "obsolete_installed_apps"
    context_processors = "context_processors"
    fields_in_custom_user_model = "fields_in_custom_user_model"


REQUIRED_INSTALLED_APPS = (
    # module name, package name, error code
    ("mptt", "django-mptt", "E001"),
    ("sekizai", "django-sekizai", "E002"),
    ("django.contrib.humanize", "django.contrib.humanize", "E003"),
    ("django.contrib.contenttypes", "django.contrib.contenttypes", "E004"),
    ("django.contrib.sites", "django.contrib.sites", "E005"),
)

OBSOLETE_INSTALLED_APPS = (
    # obsolete module name, new module name, error code
    ("django_notify", "django_nyt", "E006"),
)

REQUIRED_CONTEXT_PROCESSORS = (
    # context processor name, error code
    ("django.contrib.auth.context_processors.auth", "E007"),
    ("django.template.context_processors.request", "E008"),
    ("sekizai.context_processors.sekizai", "E009"),
)

FIELDS_IN_CUSTOM_USER_MODEL = (
    # check function, field fetcher, required field type, error code
    ("check_user_field", "USERNAME_FIELD", "CharField", "E010"),
    ("check_email_field", "get_email_field_name()", "EmailField", "E011"),
)


def check_for_required_installed_apps(app_configs, **kwargs):
    errors = []
    for app in REQUIRED_INSTALLED_APPS:
        if not apps.is_installed(app[0]):
            errors.append(
                Error("needs %s in INSTALLED_APPS" % app[1], id="wiki.%s" % app[2],)
            )
    return errors


def check_for_obsolete_installed_apps(app_configs, **kwargs):
    errors = []
    for app in OBSOLETE_INSTALLED_APPS:
        if apps.is_installed(app[0]):
            errors.append(
                Error(
                    "You need to change from %s to %s in INSTALLED_APPS and your urlconfig."
                    % (app[0], app[1]),
                    id="wiki.%s" % app[2],
                )
            )
    return errors


def check_for_context_processors(app_configs, **kwargs):
    errors = []
    context_processors = Engine.get_default().context_processors
    for context_processor in REQUIRED_CONTEXT_PROCESSORS:
        if context_processor[0] not in context_processors:
            errors.append(
                Error(
                    "needs %s in TEMPLATE['OPTIONS']['context_processors']"
                    % context_processor[0],
                    id="wiki.%s" % context_processor[1],
                )
            )
    return errors


def check_for_fields_in_custom_user_model(app_configs, **kwargs):
    errors = []
    from wiki.conf import settings

    if not settings.ACCOUNT_HANDLING:
        return errors
    import wiki.forms_account_handling
    from django.contrib.auth import get_user_model

    User = get_user_model()
    for (
        check_function_name,
        field_fetcher,
        required_field_type,
        error_code,
    ) in FIELDS_IN_CUSTOM_USER_MODEL:
        function = getattr(wiki.forms_account_handling, check_function_name)
        if not function(User):
            errors.append(
                Error(
                    "%s.%s.%s refers to a field that is not of type %s"
                    % (
                        User.__module__,
                        User.__name__,
                        field_fetcher,
                        required_field_type,
                    ),
                    hint="If you have your own login/logout views, turn off settings.WIKI_ACCOUNT_HANDLING",
                    obj=User,
                    id="wiki.%s" % error_code,
                )
            )
    return errors
