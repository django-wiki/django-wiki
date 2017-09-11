from __future__ import absolute_import, unicode_literals

from django.conf import settings as django_settings

SLUG = 'inputs'

INPUTS = getattr(
    django_settings,
    'WIKI_PLUGINS_INPUTS',
    ('text', 'text_inline',
     'password', 'password_inline',
     'file',
     'files',
     'textarea',
     ))
