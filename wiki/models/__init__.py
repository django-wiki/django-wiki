# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import warnings

from urlpath import URLPath
from article import Article, ArticleRevision

######################
# Configuration stuff
######################

if not 'mptt' in settings.INSTALLED_APPS:
    raise ImproperlyConfigured('django-wiki: needs mptt in INSTALLED_APPS')

######################
# Warnings
######################

if not 'south' in settings.INSTALLED_APPS:
    warnings.warn("django-wiki: No south in your INSTALLED_APPS. This is highly discouraged.")