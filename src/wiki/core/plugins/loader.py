# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from django.utils.module_loading import autodiscover_modules


def load_wiki_plugins():
    autodiscover_modules('wiki_plugin')
