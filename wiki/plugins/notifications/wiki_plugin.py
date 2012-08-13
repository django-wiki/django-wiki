from wiki.core import plugins_registry
from wiki import plugins

class NotifyPlugin(plugins.BasePlugin):
    
    settings_form = 'wiki.plugins.notifications.forms.SubscriptionForm'
    
    def __init__(self):
        #print "I WAS LOADED!"
        pass
    

plugins_registry.register(NotifyPlugin)