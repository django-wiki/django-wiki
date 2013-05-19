import sys
from django.conf import settings

settings.configure(
    DEBUG=True,
    AUTH_USER_MODEL='testdata.CustomUser',
    DATABASES={
         'default': {
             'ENGINE': 'django.db.backends.sqlite3',
         }
    },
    SITE_ID=1,
    ROOT_URLCONF='wiki.tests.testdata.urls',
    INSTALLED_APPS=(
        'wiki.tests.testdata',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'django.contrib.humanize',
        'django.contrib.sites',
        'south',
        'django_notify',
        'mptt',
        'sekizai',
        'sorl.thumbnail',
        'wiki',
        'wiki.plugins.attachments',
        'wiki.plugins.notifications',
        'wiki.plugins.images',
        'wiki.plugins.macros',
    ),
    TEMPLATE_CONTEXT_PROCESSORS=(
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.request",
        "django.core.context_processors.static",
        "django.core.context_processors.tz",
        "django.contrib.messages.context_processors.messages",
        "sekizai.context_processors.sekizai",
    ),
    USE_TZ=True,
    SOUTH_TESTS_MIGRATE=True,
)

from django.test.simple import DjangoTestSuiteRunner
test_runner = DjangoTestSuiteRunner(verbosity=1)

# If you use South for migrations, uncomment this to monkeypatch
# syncdb to get migrations to run.
from south.management.commands import patch_for_test_db_setup
patch_for_test_db_setup()

failures = test_runner.run_tests(['wiki', ])
if failures:
    sys.exit(failures)