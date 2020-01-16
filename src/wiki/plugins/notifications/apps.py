from django.apps import AppConfig
from django.db.models import signals
from django.utils.translation import gettext_lazy as _


class NotificationsConfig(AppConfig):
    name = "wiki.plugins.notifications"
    verbose_name = _("Wiki notifications")
    label = "wiki_notifications"

    def ready(self):
        """
        NOTIFICATIONS FOR PLUGINS
        """
        from django_nyt.utils import notify
        from wiki.core.plugins import registry
        from wiki.decorators import disable_signal_for_loaddata
        from . import models

        for plugin in registry.get_plugins():

            notifications = getattr(plugin, "notifications", [])
            for notification_dict in notifications:

                @disable_signal_for_loaddata
                def plugin_notification(instance, **kwargs):
                    if notification_dict.get("ignore", lambda x: False)(instance):
                        return
                    if kwargs.get("created", False) == notification_dict.get(
                        "created", True
                    ):
                        if "get_url" in notification_dict:
                            url = notification_dict["get_url"](instance)
                        else:
                            url = models.default_url(
                                notification_dict["get_article"](instance)
                            )

                        message = notification_dict["message"](instance)
                        notify(
                            message,
                            notification_dict["key"],
                            target_object=notification_dict["get_article"](instance),
                            url=url,
                        )

                signals.post_save.connect(
                    plugin_notification, sender=notification_dict["model"]
                )
