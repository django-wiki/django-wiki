from django.apps import apps
from django.core.checks import Error
from wiki.compat import get_default_engine


class Tags:
    required_installed_apps = "required_installed_apps"
    obsolete_installed_apps = "obsolete_installed_apps"
    context_processors = "context_processors"


REQUIRED_INSTALLED_APPS = (
    # module name, package name, error code
    ('mptt', 'django-mptt', 'E001'),
    ('sekizai', 'django-sekizai', 'E002'),
    ('django.contrib.humanize', 'django.contrib.humanize', 'E003'),
    ('django.contrib.contenttypes', 'django.contrib.contenttypes', 'E004'),
    ('django.contrib.sites', 'django.contrib.sites', 'E005'),
)

OBSOLETE_INSTALLED_APPS = (
    # obsolete module name, new module name, error code
    ('django_notify', 'django_nyt', 'E006'),
)

REQUIRED_CONTEXT_PROCESSORS = (
    # context processor name, error code
    ('django.contrib.auth.context_processors.auth', 'E007'),
    ('django.template.context_processors.request', 'E008'),
    ('sekizai.context_processors.sekizai', 'E009'),
)


def check_for_required_installed_apps(app_configs, **kwargs):
    errors = []
    for app in REQUIRED_INSTALLED_APPS:
        if not apps.is_installed(app[0]):
            errors.append(
                Error(
                    'needs %s in INSTALLED_APPS' % app[1],
                    id='wiki.%s' % app[2],
                )
            )
    return errors


def check_for_obsolete_installed_apps(app_configs, **kwargs):
    errors = []
    for app in OBSOLETE_INSTALLED_APPS:
        if apps.is_installed(app[0]):
            errors.append(
                Error(
                    'You need to change from %s to %s in INSTALLED_APPS and your urlconfig.' % (app[0], app[1]),
                    id='wiki.%s' % app[2],
                )
            )
    return errors


def check_for_context_processors(app_configs, **kwargs):
    errors = []
    context_processors = get_default_engine().context_processors
    for context_processor in REQUIRED_CONTEXT_PROCESSORS:
        if context_processor[0] not in context_processors:
            errors.append(
                Error(
                    "needs %s in TEMPLATE['OPTIONS']['context_processors']" % context_processor[0],
                    id='wiki.%s' % context_processor[1],
                )
            )
    return errors
