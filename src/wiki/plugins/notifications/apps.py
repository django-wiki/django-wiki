from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NotificationsConfig(AppConfig):
    name = 'wiki.plugins.notifications'
    verbose_name = _("Wiki notifications")
    label = 'wiki_notifications'
