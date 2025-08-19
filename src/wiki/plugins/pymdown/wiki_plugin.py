from django.utils.translation import gettext as _
from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
from wiki.plugins.pymdown import settings


class PymdownPlugin(BasePlugin):
    slug = settings.SLUG

    sidebar = {
        "headline": _("PyMdown Macros"),
        "icon_class": "fa-play",
        "template": "wiki/plugins/pymdown/sidebar.html",
        "form_class": None,
        "get_form_kwargs": (lambda a: {}),
    }

    # Skipping tabs as for now they do not work
    markdown_extensions = [
        "pymdownx.blocks.admonition",
        "pymdownx.blocks.definition",
        "pymdownx.blocks.html",
        "pymdownx.blocks.details",
    ]


settings.update_whitelist()

registry.register(PymdownPlugin)
