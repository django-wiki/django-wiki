# -*- coding: utf-8 -*-
from django.conf import settings as django_settings

# Should urls be case sensitive?
URL_CASE_SENSITIVE = getattr(django_settings, "WIKI_URL_CASE_SENSITIVE", False)