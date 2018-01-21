from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NotificationsConfig(AppConfig):
    name = 'wiki.plugins.notifications'
    verbose_name = _("Wiki notifications")
    label = 'wiki_notifications'
