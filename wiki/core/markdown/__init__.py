from __future__ import absolute_import, unicode_literals

from wiki.conf import settings
from wiki.core.markdown.mdx.previewlinks import PreviewLinksExtension
from wiki.core.markdown.mdx.responsivetable import ResponsiveTableExtension
from wiki.core.plugins import registry as plugin_registry
import markdown


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


def article_markdown(text, article, *args, **kwargs):
    md = ArticleMarkdown(article, *args, **kwargs)
    return md.convert(text)
