from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin


class Plugin(BasePlugin):

    markdown_extensions = [
        'wiki.plugins.redlinks.mdx.redlinks',
    ]


registry.register(Plugin)
