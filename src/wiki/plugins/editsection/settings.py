from __future__ import absolute_import, unicode_literals

from django.conf import settings as django_settings

SLUG = 'editsection'

#: Add "[edit]" links to all section headers till this level. By using
#: these links editing only the text from the selected section is possible.
MAX_LEVEL = getattr(django_settings, 'WIKI_EDITSECTION_MAX_LEVEL', 3)
