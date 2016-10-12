# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
from six import string_types, text_type

# TODO: Don't use wildcards
from .article import *  # noqa
from .pluginbase import *  # noqa
from .urlpath import *  # noqa
from django.utils.functional import lazy

# TODO: Should the below stuff be executed a more logical place?
# Follow Django's default_settings.py / settings.py pattern and put these
# in d_s.py? That might be confusing, though.

######################
# Configuration stuff
######################

if 'mptt' not in django_settings.INSTALLED_APPS:
    raise ImproperlyConfigured('django-wiki: needs mptt in INSTALLED_APPS')

if 'sekizai' not in django_settings.INSTALLED_APPS:
    raise ImproperlyConfigured('django-wiki: needs sekizai in INSTALLED_APPS')

# if not 'django_nyt' in django_settings.INSTALLED_APPS:
#    raise ImproperlyConfigured('django-wiki: needs django_nyt in INSTALLED_APPS')

if 'django.contrib.humanize' not in django_settings.INSTALLED_APPS:
    raise ImproperlyConfigured(
        'django-wiki: needs django.contrib.humanize in INSTALLED_APPS')

if 'django.contrib.contenttypes' not in django_settings.INSTALLED_APPS:
    raise ImproperlyConfigured(
        'django-wiki: needs django.contrib.contenttypes in INSTALLED_APPS')

if 'django.contrib.sites' not in django_settings.INSTALLED_APPS:
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

if 'django.contrib.auth.context_processors.auth' not in TEMPLATE_CONTEXT_PROCESSORS:
    raise ImproperlyConfigured(
        'django-wiki: needs django.contrib.auth.context_processors.auth in TEMPLATE_CONTEXT_PROCESSORS')

if not any(s in TEMPLATE_CONTEXT_PROCESSORS for s in ['django.core.context_processors.request',
                                                      'django.template.context_processors.request']):
    raise ImproperlyConfigured(
        'django-wiki: needs django.core.context_processors.request or django.template.context_processors.request in TEMPLATE_CONTEXT_PROCESSORS')

if 'django_notify' in django_settings.INSTALLED_APPS:
    raise ImproperlyConfigured(
        'django-wiki: You need to change from django_notify to django_nyt in INSTALLED_APPS and your urlconfig.')


from django.core import urlresolvers  # noqa

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
reverse_lazy = lazy(reverse, text_type)
urlresolvers.reverse = reverse
urlresolvers.reverse_lazy = reverse_lazy

# Patch up other locations of the reverse function
try:
    from django.urls import base
    from django import urls
    from django import shortcuts
    base.reverse = reverse
    base.reverse_lazy = reverse_lazy
    urls.reverse = reverse
    urls.reverse_lazy = reverse_lazy
    shortcuts.reverse = reverse
    urls.reverse_lazy = reverse_lazy
except ImportError:
    pass
