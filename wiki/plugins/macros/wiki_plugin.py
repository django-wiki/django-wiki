# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _

from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
from wiki.plugins.macros import settings
from wiki.plugins.macros.markdown_extensions import MacroExtension


class MacroPlugin(BasePlugin):
    
    slug = settings.SLUG
    
    sidebar = {'headline': _('Macros'),
               'icon_class': 'icon-play',
               'template': 'wiki/plugins/macros/sidebar.html',
               'form_class': None,
               'get_form_kwargs': (lambda a: {})}
    
    markdown_extensions = [MacroExtension()]
    
    def __init__(self):
        pass
    
registry.register(MacroPlugin)
