# -*- coding: utf-8 -*-
from os import path as os_path
PROJECT_PATH = os_path.abspath(os_path.split(os_path.dirname(__file__))[0])

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'prepopulated.db',  # Or path to database file if using sqlite3.
    }
}

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Europe/Copenhagen'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-dk'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os_path.join(PROJECT_PATH, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os_path.join(PROJECT_PATH, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'testproject.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'testproject.wsgi.application'

TEMPLATE_DIRS = (
    os_path.join(PROJECT_PATH, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'sekizai.context_processors.sekizai',
]

INSTALLED_APPS = [
    'django.contrib.humanize',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'sekizai',
    'sorl.thumbnail',
    'django_nyt',
    'wiki',
    'wiki.plugins.macros',
    'wiki.plugins.help',
    'wiki.plugins.links',
    'wiki.plugins.images',
    'wiki.plugins.attachments',
    'wiki.plugins.notifications',
    'mptt',
]
from django import VERSION
if VERSION < (1, 7):
    INSTALLED_APPS.append('south')
    SOUTH_MIGRATION_MODULES = {
        'django_nyt': 'django_nyt.south_migrations',
        'wiki': 'wiki.south_migrations',
        'images': 'wiki.plugins.images.south_migrations',
        'notifications': 'wiki.plugins.notifications.south_migrations',
        'attachments': 'wiki.plugins.attachments.south_migrations',
    }
else:
    TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

WIKI_ANONYMOUS_WRITE = True
WIKI_ANONYMOUS_CREATE = False

# Do not user /accounts/profile as default
#LOGIN_REDIRECT_URL = "/"
from django.core.urlresolvers import reverse_lazy
LOGIN_REDIRECT_URL = reverse_lazy('wiki:get', kwargs={'path': ''})


try:
    import debug_toolbar #@UnusedImport
    MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES) + [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
    INSTALLED_APPS = list(INSTALLED_APPS) + ['debug_toolbar']
    INTERNAL_IPS = ('127.0.0.1',)
    DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
except ImportError:
    pass


# "Secret" key for the prepopulated db
SECRET_KEY = 'b^fv_)t39h%9p40)fnkfblo##jkr!$0)lkp6bpy!fi*f$4*92!'

try:
    from testproject.settings.local import *
except ImportError:
    pass
