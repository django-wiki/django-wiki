from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NotifcationsConfig(AppConfig):
    name = 'wiki.plugins.notifications'
    verbose_name = _("Wiki notifications")
    label = 'wiki_notifications'


class ImagesConfig(AppConfig):
    name = 'wiki.plugins.images'
    verbose_name = _("Wiki images")
    label = 'wiki_images'


class AttachmentsConfig(AppConfig):
    name = 'wiki.plugins.attachments'
    verbose_name = _("Wiki attachments")
    label = 'wiki_attachments'
