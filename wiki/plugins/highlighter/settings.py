from django.conf import settings as django_settings

LOOKUP_LEVEL = getattr(django_settings, 'WIKI_LINKS_LOOKUP_LEVEL', 2)
