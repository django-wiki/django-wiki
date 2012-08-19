from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin

class NotifyPlugin(BasePlugin):
    
    settings_form = 'wiki.plugins.notifications.forms.SubscriptionForm'
    
    def __init__(self):
        pass

registry.register(NotifyPlugin)