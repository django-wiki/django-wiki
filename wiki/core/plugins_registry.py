# -*- coding: utf-8 -*-
from django.utils.importlib import import_module

_cache = {}
_settings_forms = []
_markdown_extensions = []
_article_tabs = []
_sidebar = []

def register(PluginClass):
    """
    Register a plugin class. This function will call back your plugin's
    constructor.
    """
    if PluginClass in _cache.keys():
        raise Exception("Plugin class already registered")
    plugin = PluginClass()
    _cache[PluginClass] = plugin
    
    settings_form = getattr(PluginClass, 'settings_form', None)
    if settings_form:
        if isinstance(settings_form, basestring):
            klassname = settings_form.split(".")[-1]
            modulename = ".".join(settings_form.split(".")[:-1])
            form_module = import_module(modulename)
            settings_form = getattr(form_module, klassname)
        _settings_forms.append(settings_form)
    
    
    if getattr(PluginClass, 'article_tab', None):
        _article_tabs.append(plugin)
    
    if getattr(PluginClass, 'sidebar', None):
        _sidebar.append(plugin)

    _markdown_extensions.extend(getattr(PluginClass, 'markdown_extensions', []))        
    
def get_plugins():
    return _cache

def get_markdown_extensions():
    return _markdown_extensions

def get_article_tabs():
    """Returns plugin classes that should connect to the article tab menu"""
    return _article_tabs

def get_sidebar():
    """Returns plugin classes that should connect to the sidebar"""
    return _sidebar
