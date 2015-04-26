# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.conf import settings as django_settings

DISQUS_SORTNAME = getattr(django_settings, 'WIKI_DISQUS_SORTNAME', '')
