from __future__ import absolute_import, unicode_literals

import bleach
import markdown

from wiki.conf import settings
from wiki.core.markdown.mdx.previewlinks import PreviewLinksExtension
from wiki.core.markdown.mdx.responsivetable import ResponsiveTableExtension
from wiki.core.plugins import registry as plugin_registry


class ArticleMarkdown(markdown.Markdown):

    def __init__(self, article, preview=False, *args, **kwargs):
        kwargs = settings.MARKDOWN_KWARGS
        kwargs['extensions'] = self.get_markdown_extensions()
        markdown.Markdown.__init__(self, *args, **kwargs)
        self.article = article
        self.preview = preview

    def core_extensions(self):
        """List of core extensions found in the mdx folder"""
        return [PreviewLinksExtension(), ResponsiveTableExtension()]

    def get_markdown_extensions(self):
        kwargs = settings.MARKDOWN_KWARGS
        extensions = list(kwargs.get('extensions', []))
        extensions += self.core_extensions()
        extensions += plugin_registry.get_markdown_extensions()
        return extensions

    def convert(self, text, *args, **kwargs):
        text = bleach.clean(text, tags=settings.MARKDOWN_HTML_WHITELIST)
        return super(ArticleMarkdown, self).convert(text, *args, **kwargs)


def article_markdown(text, article, *args, **kwargs):
    md = ArticleMarkdown(article, *args, **kwargs)
    return md.convert(text)
