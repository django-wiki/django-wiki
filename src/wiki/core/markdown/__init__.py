import bleach
import markdown
from bleach.css_sanitizer import CSSSanitizer
from wiki.conf import settings
from wiki.core.plugins import registry as plugin_registry


class ArticleMarkdown(markdown.Markdown):
    def __init__(self, article, preview=False, user=None, *args, **kwargs):
        kwargs.update(settings.MARKDOWN_KWARGS)
        kwargs["extensions"] = self.get_markdown_extensions()
        super().__init__(*args, **kwargs)
        self.article = article
        self.preview = preview
        self.user = user
        self.source = None

    def core_extensions(self):
        """List of core extensions found in the mdx folder"""
        return [
            "wiki.core.markdown.mdx.codehilite",
            "wiki.core.markdown.mdx.previewlinks",
            "wiki.core.markdown.mdx.responsivetable",
        ]

    def get_markdown_extensions(self):
        extensions = list(settings.MARKDOWN_KWARGS.get("extensions", []))
        extensions += self.core_extensions()
        extensions += plugin_registry.get_markdown_extensions()
        return extensions

    def convert(self, text, *args, **kwargs):
        # store source in instance, for extensions which might need it
        self.source = text
        html = super().convert(text, *args, **kwargs)
        if settings.MARKDOWN_SANITIZE_HTML:
            tags = settings.MARKDOWN_HTML_WHITELIST.union(
                plugin_registry.get_html_whitelist()
            )

            css_sanitizer = CSSSanitizer(
                allowed_css_properties=settings.MARKDOWN_HTML_STYLES
            )

            attrs = {}
            attrs.update(settings.MARKDOWN_HTML_ATTRIBUTES)
            attrs.update(plugin_registry.get_html_attributes().items())

            html = bleach.clean(
                html,
                tags=tags,
                attributes=attrs,
                css_sanitizer=css_sanitizer,
                strip=True,
            )
        return html


def article_markdown(text, article, *args, **kwargs):
    md = ArticleMarkdown(article, *args, **kwargs)
    return md.convert(text)


def add_to_registry(processor, key, value, location):
    """Utility function to register a key by location to Markdown's registry.

    Parameters:
    * `processor`: Markdown Registry instance
    * `key`: A string used to reference the item.
    * `value`: The item being registered.
    * `location`: Where to register the new key

    location can be one of the strings below:
    * _begin (registers the key as the highest priority)
    * _end (registers the key as the lowest priority)
    * a string that starts with `<` or `>` (sets priority halfway between existing priorities)

    Returns: None
    Raises: ValueError if location is an invalid string.
    """

    if len(processor) == 0:
        # This is the first item. Set priority to 50.
        priority = 50
    elif location == "_begin":
        processor._sort()
        # Set priority 5 greater than highest existing priority
        priority = processor._priority[0].priority + 5
    elif location == "_end":
        processor._sort()
        # Set priority 5 less than lowest existing priority
        priority = processor._priority[-1].priority - 5
    elif location.startswith("<") or location.startswith(">"):
        # Set priority halfway between existing priorities.
        i = processor.get_index_for_name(location[1:])
        if location.startswith("<"):
            after = processor._priority[i].priority
            if i > 0:
                before = processor._priority[i - 1].priority
            else:
                # Location is first item`
                before = after + 10
        else:
            # location.startswith('>')
            before = processor._priority[i].priority
            if i < len(processor) - 1:
                after = processor._priority[i + 1].priority
            else:
                # location is last item
                after = before - 10
        priority = before - ((before - after) / 2)
    else:
        raise ValueError(
            'Not a valid location: "%s". Location key '
            'must start with a ">" or "<".' % location
        )
    processor.register(value, key, priority)
