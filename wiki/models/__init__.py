from __future__ import absolute_import
from __future__ import unicode_literals
# -*- coding: utf-8 -*-

from django import VERSION
from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
import warnings
from six import string_types

# TODO: Don't use wildcards
from .article import *
from .pluginbase import *
from .urlpath import *

# TODO: Should the below stuff be executed a more logical place?
# Follow Django's default_settings.py / settings.py pattern and put these
# in d_s.py? That might be confusing, though.

######################
# Configuration stuff
######################

if not 'mptt' in django_settings.INSTALLED_APPS:
    raise ImproperlyConfigured('django-wiki: needs mptt in INSTALLED_APPS')

if not 'sekizai' in django_settings.INSTALLED_APPS:
    raise ImproperlyConfigured('django-wiki: needs sekizai in INSTALLED_APPS')

# if not 'django_nyt' in django_settings.INSTALLED_APPS:
#    raise ImproperlyConfigured('django-wiki: needs django_nyt in INSTALLED_APPS')

if not 'django.contrib.humanize' in django_settings.INSTALLED_APPS:
    raise ImproperlyConfigured(
        'django-wiki: needs django.contrib.humanize in INSTALLED_APPS')

if not 'django.contrib.contenttypes' in django_settings.INSTALLED_APPS:
    raise ImproperlyConfigured(
        'django-wiki: needs django.contrib.contenttypes in INSTALLED_APPS')

if not 'django.contrib.sites' in django_settings.INSTALLED_APPS:
    raise ImproperlyConfigured(
        'django-wiki: needs django.contrib.sites in INSTALLED_APPS')

# Need to handle Django 1.8 'TEMPLATES', recognizing that users may still be
# using 1.7 conventions/settings with 1.8.
TEMPLATE_CONTEXT_PROCESSORS = getattr(django_settings, 'TEMPLATE_CONTEXT_PROCESSORS', [])
if hasattr(django_settings, 'TEMPLATES'):
    # Django 1.8 compat
    backends = [b for b in django_settings.TEMPLATES if b.get('BACKEND', '') == 'django.template.backends.django.DjangoTemplates']
    if len(backends) == 1:
        TEMPLATE_CONTEXT_PROCESSORS = backends[0].get('OPTIONS', {}).get('context_processors', [])

if not 'django.contrib.auth.context_processors.auth' in django_settings.TEMPLATE_CONTEXT_PROCESSORS:
    raise ImproperlyConfigured(
        'django-wiki: needs django.contrib.auth.context_processors.auth in TEMPLATE_CONTEXT_PROCESSORS')

if not any(s in TEMPLATE_CONTEXT_PROCESSORS for s in ['django.core.context_processors.request',
                                                      'django.template.context_processors.request']):
    raise ImproperlyConfigured(
        'django-wiki: needs django.core.context_processors.request or django.template.context_processors.request in TEMPLATE_CONTEXT_PROCESSORS')

if 'django_notify' in django_settings.INSTALLED_APPS:
    raise ImproperlyConfigured(
        'django-wiki: You need to change from django_notify to django_nyt in INSTALLED_APPS and your urlconfig.')

######################
# Warnings
######################


if VERSION < (1, 7):
    if 'south' not in django_settings.INSTALLED_APPS:
        warnings.warn(
            "django-wiki: No south in your INSTALLED_APPS. This is highly discouraged.")


from django.core import urlresolvers

original_django_reverse = urlresolvers.reverse


def reverse(*args, **kwargs):
    """Now this is a crazy and silly hack, but it is basically here to
    enforce that an empty path always takes precedence over an article_id
    such that the root article doesn't get resolved to /ID/ but /.

    Another crazy hack that this supports is transforming every wiki url
    by a function. If _transform_url is set on this function, it will
    return the result of calling reverse._transform_url(reversed_url)
    for every url in the wiki namespace.
    """
    if isinstance(args[0], string_types) and args[0].startswith('wiki:'):
        url_kwargs = kwargs.get('kwargs', {})
        path = url_kwargs.get('path', False)
        # If a path is supplied then discard the article_id
        if path is not False:
            url_kwargs.pop('article_id', None)
            url_kwargs['path'] = path
            kwargs['kwargs'] = url_kwargs

        url = original_django_reverse(*args, **kwargs)
        if hasattr(reverse, '_transform_url'):
            url = reverse._transform_url(url)
    else:
        url = original_django_reverse(*args, **kwargs)

    return url

# Now we redefine reverse method
urlresolvers.reverse = reverse
