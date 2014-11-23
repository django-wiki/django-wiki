# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
from wiki.plugins.preview.mdx.previewlinksblank import makeExtension as linkExtension


class PreviewPlugin(BasePlugin):

    slug = 'preview'
    markdown_extensions = [linkExtension()]

registry.register(PreviewPlugin)
