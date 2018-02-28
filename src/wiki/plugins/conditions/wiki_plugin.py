from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext as _
from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
from wiki.plugins.conditions import settings
from wiki.plugins.conditions.mdx.condition import ConditionExtension


class ConditionPlugin(BasePlugin):
    slug = settings.SLUG

    sidebar = {'headline': _('Conditions'),
               'icon_class': 'fa-question-circle',
               'template': 'wiki/plugins/conditions/sidebar.html',
               'form_class': None,
               'get_form_kwargs': (lambda a: {})}

    markdown_extensions = [
        ConditionExtension(),
    ]


registry.register(ConditionPlugin)
