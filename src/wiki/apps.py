from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class WikiConfig(AppConfig):
    name = "wiki"
    verbose_name = _("Wiki")
