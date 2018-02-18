from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AttachmentsConfig(AppConfig):
    name = 'wiki.plugins.attachments'
    verbose_name = _("Wiki attachments")
    label = 'wiki_attachments'
