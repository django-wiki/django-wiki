from django.utils.translation import gettext as _
from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin


class HelpPlugin(BasePlugin):

    slug = 'help'

    sidebar = {'headline': _('Help'),
               'icon_class': 'fa-question-circle',
               'template': 'wiki/plugins/help/sidebar.html',
               'form_class': None,
               'get_form_kwargs': (lambda a: {})}

    markdown_extensions = []


registry.register(HelpPlugin)
