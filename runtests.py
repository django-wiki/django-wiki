#!/usr/bin/env python
import sys
import django
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


# If you use South for migrations, uncomment this to monkeypatch
# syncdb to get migrations to run.
from south.management.commands import patch_for_test_db_setup
patch_for_test_db_setup()

from django.core.management import execute_from_command_line
argv = [sys.argv[0], "test"]

if len(sys.argv) == 1:
    # Nothing following 'runtests.py':
    if django.VERSION < (1,6):
        argv.append("wiki")
    else:
        argv.append("wiki.tests")
else:
    # Allow tests to be specified:
    argv.extend(sys.argv[1:])

execute_from_command_line(argv)
