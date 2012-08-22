# -*- coding: utf-8 -*-

from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
import warnings

# TODO: Don't use wildcards
from article import *
from urlpath import *

# TODO: Should the below stuff be executed a more logical place?

######################
# Configuration stuff
######################

if not 'mptt' in django_settings.INSTALLED_APPS:
    raise ImproperlyConfigured('django-wiki: needs mptt in INSTALLED_APPS')

if not 'sekizai' in django_settings.INSTALLED_APPS:
    raise ImproperlyConfigured('django-wiki: needs sekizai in INSTALLED_APPS')

if not 'django_notify' in django_settings.INSTALLED_APPS:
    raise ImproperlyConfigured('django-wiki: needs django_notify in INSTALLED_APPS')

if not 'django.contrib.humanize' in django_settings.INSTALLED_APPS:
    raise ImproperlyConfigured('django-wiki: needs django.contrib.humanize in INSTALLED_APPS')

if not 'django.contrib.contenttypes' in django_settings.INSTALLED_APPS:
    raise ImproperlyConfigured('django-wiki: needs django.contrib.contenttypes in INSTALLED_APPS')

if not 'django.contrib.auth.context_processors.auth' in django_settings.TEMPLATE_CONTEXT_PROCESSORS:
    raise ImproperlyConfigured('django-wiki: needs django.contrib.auth.context_processors.auth in TEMPLATE_CONTEXT_PROCESSORS')

######################
# Warnings
######################

if not 'south' in django_settings.INSTALLED_APPS:
    warnings.warn("django-wiki: No south in your INSTALLED_APPS. This is highly discouraged.")


######################
# PLUGINS
######################

from wiki.core.plugins.loader import load_wiki_plugins

load_wiki_plugins()


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
    if isinstance(args[0], basestring) and args[0].startswith('wiki:'):
        url_kwargs = kwargs.get('kwargs', {})
        path = url_kwargs.get('path', False)
        # If a path is supplied then discard the article_id
        if path != False:
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