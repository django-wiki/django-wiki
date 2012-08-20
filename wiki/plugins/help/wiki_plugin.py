# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns
from django.utils.translation import ugettext as _

from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin

class HelpPlugin(BasePlugin):
    
    slug = 'help'
    urlpatterns = patterns('',)
    
    sidebar = {'headline': _('Help'),
               'icon_class': 'icon-question-sign',
               'template': 'wiki/plugins/help/sidebar.html',
               'form_class': None,
               'get_form_kwargs': (lambda a: {})}
    
    markdown_extensions = []
    
    def __init__(self):
        pass
    
registry.register(HelpPlugin)

