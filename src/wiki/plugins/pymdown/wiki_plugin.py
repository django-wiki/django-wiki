from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
from wiki.plugins.pymdown import settings


class Plugin(BasePlugin):

    # Skipping tabs as for now they do not work
    markdown_extensions = [
        "pymdownx.blocks.admonition",
        "pymdownx.blocks.definition",
        "pymdownx.blocks.html",
        "pymdownx.blocks.details",
    ]


settings.update_whitelist()

registry.register(Plugin)
