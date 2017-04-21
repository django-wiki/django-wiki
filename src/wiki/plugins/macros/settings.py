from __future__ import absolute_import, unicode_literals

from django.conf import settings as django_settings

SLUG = 'macros'
APP_LABEL = 'wiki'

METHODS = getattr(
    django_settings,
    'WIKI_PLUGINS_METHODS',
    ('article_list',
     'toc',
     ))
