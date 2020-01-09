from django.utils.translation import gettext as _
from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
from wiki.plugins.macros import settings


class MacroPlugin(BasePlugin):

    slug = settings.SLUG

    sidebar = {
        "headline": _("Macros"),
        "icon_class": "fa-play",
        "template": "wiki/plugins/macros/sidebar.html",
        "form_class": None,
        "get_form_kwargs": (lambda a: {}),
    }

    markdown_extensions = [
        "wiki.plugins.macros.mdx.macro",
        "wiki.plugins.macros.mdx.toc",
        "wiki.plugins.macros.mdx.wikilinks",
    ]


registry.register(MacroPlugin)
