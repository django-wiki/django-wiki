# -*- coding: utf-8 -*-
from os import path as os_path
import os

PROJECT_PATH = os_path.abspath(os_path.split(__file__)[0])
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

#from django.core.urlresolvers import reverse_lazy
#LOGIN_REDIRECT_URL = reverse_lazy('wiki:get', kwargs={'path': ''})

# This forces the wiki login view to redirect to the referer...
LOGIN_REDIRECT_URL = None
LOGIN_URL = '/_accounts/login/'
LOGOUT_URL = '/_accounts/logout/'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os_path.join(PROJECT_PATH, 'db', 'prepopulated.db'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
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

SECRET_KEY = 'b^fv_)t39h%9p40)fnkfblo##jkr!$0)lkp6bpy!fi*f$4*92!'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'wiki.middleware.RequestCache',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'testproject.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'testproject.wsgi.application'

# See https://docs.djangoproject.com/en/1.11/ref/templates/upgrading/
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                "django.template.context_processors.request",  # TODO: is this needed?
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "sekizai.context_processors.sekizai",
            ],
            'debug': DEBUG,
        },
    },
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
    'django_notify',  # Note: this is not installed in version 0.2.x. But there is "django_nyt".
    'sorl.thumbnail',
    'wiki',
    'wiki.plugins.help',  # Note: in version 0.2.x, wiki.plugins.macro is added.
    'wiki.plugins.links',
    'wiki.plugins.images',
    'wiki.plugins.attachments',
    'wiki.plugins.notifications',
    'mptt',
]

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse'
#         }
#     },
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'filters': ['require_debug_false'],
#             'class': 'django.utils.log.AdminEmailHandler'
#         }
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     }
# }

WIKI_ANONYMOUS_WRITE = True

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
