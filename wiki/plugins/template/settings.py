from django import VERSION
from django.conf import settings as django_settings

# This is not used in django 1.7+
APP_LABEL = 'template' if VERSION < (1, 7) else None
SLUG = "template"


ANONYMOUS = getattr(django_settings, 'WIKI_ANONYMOUS', True)
ANONYMOUS_WRITE = getattr(django_settings, 'WIKI_ANONYMOUS_WRITE', False)
ANONYMOUS_CREATE = getattr(
    django_settings, 'WIKI_ANONYMOUS_CREATE', ANONYMOUS_WRITE)
