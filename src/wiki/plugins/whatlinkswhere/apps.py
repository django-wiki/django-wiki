from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WhatLinksWhereConfig(AppConfig):
    name = "wiki.plugins.whatlinkswhere"
    verbose_name = _("What links where")
    label = "wiki_whatlinkswhere"
