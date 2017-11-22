from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
from wiki.plugins.macros import settings
from wiki.plugins.macros.mdx.macro import MacroExtension
from wiki.plugins.macros.mdx.toc import WikiTocExtension
from wiki.plugins.macros.mdx.wikilinks import WikiLinkExtension


class MacroPlugin(BasePlugin):

    slug = settings.SLUG

    sidebar = {'headline': _('Macros'),
               'icon_class': 'fa-play',
               'template': 'wiki/plugins/macros/sidebar.html',
               'form_class': None,
               'get_form_kwargs': (lambda a: {})}

    markdown_extensions = [
        WikiLinkExtension(),
        MacroExtension(),
        WikiTocExtension()]


registry.register(MacroPlugin)
