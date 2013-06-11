from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin

from django.conf.urls import patterns, url

import settings, views

class NotifyPlugin(BasePlugin):
    
    slug = settings.SLUG
    urlpatterns = {
        'root': patterns('',
            url(r'^$', views.NotificationSettings.as_view(), name='notification_settings'),
        )
    }
    
    article_view = views.NotificationSettings().dispatch
    
    settings_form = 'wiki.plugins.notifications.forms.SubscriptionForm'
    
    def __init__(self):
        pass

registry.register(NotifyPlugin)