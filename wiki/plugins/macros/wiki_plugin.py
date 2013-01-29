# -*- coding: utf-8 -*-
from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
from wiki.plugins.macros import settings
from wiki.plugins.macros.markdown_extensions import MacroExtension


class MacroPlugin(BasePlugin):
    
    slug = settings.SLUG
    
    markdown_extensions = [MacroExtension()]
    
    def __init__(self):
        pass
    
registry.register(MacroPlugin)
