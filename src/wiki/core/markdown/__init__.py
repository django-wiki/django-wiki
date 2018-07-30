import bleach
import markdown
from wiki.conf import settings
from wiki.core.plugins import registry as plugin_registry


class ArticleMarkdown(markdown.Markdown):

    def __init__(self, article, preview=False, user=None, *args, **kwargs):
        kwargs.update(settings.MARKDOWN_KWARGS)
        kwargs['extensions'] = self.get_markdown_extensions()
        super().__init__(*args, **kwargs)
        self.article = article
        self.preview = preview
        self.user = user

    def core_extensions(self):
        """List of core extensions found in the mdx folder"""
        return [
            'wiki.core.markdown.mdx.codehilite',
            'wiki.core.markdown.mdx.previewlinks',
            'wiki.core.markdown.mdx.responsivetable',
        ]

    def get_markdown_extensions(self):
        extensions = list(settings.MARKDOWN_KWARGS.get('extensions', []))
        extensions += self.core_extensions()
        extensions += plugin_registry.get_markdown_extensions()
        return extensions

    def convert(self, text, *args, **kwargs):
        html = super().convert(text, *args, **kwargs)
        if settings.MARKDOWN_SANITIZE_HTML:
            tags = settings.MARKDOWN_HTML_WHITELIST + plugin_registry.get_html_whitelist()

            attrs = dict()
            attrs.update(settings.MARKDOWN_HTML_ATTRIBUTES)
            attrs.update(plugin_registry.get_html_attributes().items())

            html = bleach.clean(
                html,
                tags=tags,
                attributes=attrs,
                styles=settings.MARKDOWN_HTML_STYLES,
            )
        return html


def article_markdown(text, article, *args, **kwargs):
    md = ArticleMarkdown(article, *args, **kwargs)
    return md.convert(text)
