from wiki.core import plugins_registry, baseplugin

class NotifyPlugin(baseplugin.BasePlugin):
    
    settings_form = 'wiki.plugins.notifications.forms.SubscriptionForm'
    
    def __init__(self):
        #print "I WAS LOADED!"
        pass
    

plugins_registry.register(NotifyPlugin)