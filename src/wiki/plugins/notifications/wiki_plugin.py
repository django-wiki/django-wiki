from __future__ import unicode_literals

from django.conf.urls import url
from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin

from . import settings, views


class NotifyPlugin(BasePlugin):

    slug = settings.SLUG
    urlpatterns = {'root': [
        url(r'^$', views.NotificationSettings.as_view(), name='notification_settings'),
    ]}

    article_view = views.NotificationSettings().dispatch

    settings_form = 'wiki.plugins.notifications.forms.SubscriptionForm'


registry.register(NotifyPlugin)
