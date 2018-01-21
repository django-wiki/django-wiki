from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class WikiConfig(AppConfig):
    name = "wiki"
    verbose_name = _("Wiki")


class ImagesConfig(AppConfig):
    name = 'wiki.plugins.images'
    verbose_name = _("Wiki images")
    label = 'wiki_images'


class AttachmentsConfig(AppConfig):
    name = 'wiki.plugins.attachments'
    verbose_name = _("Wiki attachments")
    label = 'wiki_attachments'
