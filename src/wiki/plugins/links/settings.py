from __future__ import absolute_import, unicode_literals

from django.conf import settings as django_settings

LOOKUP_LEVEL = getattr(django_settings, 'WIKI_LINKS_LOOKUP_LEVEL', 2)
