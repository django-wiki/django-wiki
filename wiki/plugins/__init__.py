class Registry():
    
    def __init__(self):
        self._registry = []
    
    def register(self, plugin_instance):
        if not isinstance(plugin_instance, WikiPlugin):
            raise TypeError("That's not a WikiPlugin")
        self._registry.append(plugin_instance)

class WikiPlugin():
    pass