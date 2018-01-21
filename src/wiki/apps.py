from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class WikiConfig(AppConfig):
    name = "wiki"
    verbose_name = _("Wiki")


class AttachmentsConfig(AppConfig):
    name = 'wiki.plugins.attachments'
    verbose_name = _("Wiki attachments")
    label = 'wiki_attachments'
