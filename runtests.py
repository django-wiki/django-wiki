#!/usr/bin/env python
from __future__ import absolute_import, unicode_literals

import sys

import django
import pytest
from django.conf import settings

# Run py.tests
# Compatibility testing patches on the py-moneyed

settings_dict = dict(
    DEBUG=True,
    AUTH_USER_MODEL='testdata.CustomUser',
    WIKI_GROUP_MODEL='testdata.CustomGroup',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    SITE_ID=1,
    ROOT_URLCONF='wiki.tests.testdata.urls',
    INSTALLED_APPS=[
        'wiki.tests.testdata',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'django.contrib.humanize',
        'django.contrib.sites',
        'django_nyt',
        'mptt',
        'sekizai',
        'sorl.thumbnail',
        'wiki',
        'wiki.plugins.attachments',
        'wiki.plugins.notifications',
        'wiki.plugins.images',
        'wiki.plugins.macros',
    ] + (['south'] if django.VERSION < (1, 7) else []),
    MIDDLEWARE_CLASSES=[
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ],
    USE_TZ=True,
    SOUTH_TESTS_MIGRATE=True,
    SECRET_KEY='b^fv_)t39h%9p40)fnkfblo##jkr!$0)lkp6bpy!fi*f$4*92!',
)

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.template.context_processors.debug",
    "django.template.context_processors.i18n",
    "django.template.context_processors.media",
    "django.template.context_processors.request",
    "django.template.context_processors.static",
    "django.template.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "sekizai.context_processors.sekizai",
]

if django.VERSION < (1, 8):
    settings_dict.update(dict(
        TEMPLATE_CONTEXT_PROCESSORS=[p.replace('django.template.context_processors',
                                               'django.core.context_processors')
                                     for p in TEMPLATE_CONTEXT_PROCESSORS]
    ))
else:
    settings_dict.update(dict(
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': TEMPLATE_CONTEXT_PROCESSORS
                },
            },
        ]
    ))

settings.configure(**settings_dict)


# If you use South for migrations, uncomment this to monkeypatch
# syncdb to get migrations to run.
if django.VERSION < (1, 7):
    from south.management.commands import patch_for_test_db_setup
    patch_for_test_db_setup()

argv = [sys.argv[0], "test", "--traceback"]

# python setup.py test calls script with just 'test'
if len(sys.argv) == 1 or sys.argv[1] == 'test':
    # Nothing following 'runtests.py':
    if django.VERSION < (1, 6):
        argv.extend(["wiki", "attachments"])
    else:
        argv.extend(["wiki.tests", "wiki.plugins.attachments.tests"])
else:
    # Allow tests to be specified:
    argv.extend(sys.argv[1:])


failures = pytest.main()

if failures:
    sys.exit(failures)
