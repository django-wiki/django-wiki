from wiki.core import plugins_registry

import forms

class NotifyPlugin(plugins_registry.BasePlugin):
    
    settings_form = forms.SubscriptionForm
    
    def __init__(self):
        #print "I WAS LOADED!"
        pass
    

plugins_registry.register(NotifyPlugin)