from django.utils.translation import gettext as _
from django.conf import settings as django_settings
from wiki.conf import settings

SLUG = "pymdown"
APP_LABEL = "wiki"


def update_whitelist():
    setattr(
        settings,
        "MARKDOWN_HTML_WHITELIST",
        getattr(settings, "MARKDOWN_HTML_WHITELIST", frozenset()).union(
            {"details", "summary"}
        ),
    )

    updated_dict = getattr(settings, "MARKDOWN_HTML_ATTRIBUTES", {})
    updated_dict.update(
        {"details": ["class"]},
    )
    setattr(
        settings,
        "MARKDOWN_HTML_ATTRIBUTES",
        updated_dict,
    )

    # This looks for 'PYMDOWNX_KEYWORD_ARGUMENTS' in the settings.py Django file and uses it to update the
    # 'extensions_configs' key in the MARKDOWN_KWARGS which is used when creating the Markdown object.
    # This can be used to set custom arguments for PyMdown extensions
    settings.MARKDOWN_KWARGS["extension_configs"].update(
        getattr(django_settings, "PYMDOWNX_KEYWORD_ARGUMENTS", dict())
    )


pymdown_docs = [
    {
        "short_description": _("Admonition"),
        "help_text": _(
            """Insert an Admonition html tag. <a href="https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/admonition/" target="_blank">Open external docs ↗</a>"""
        ),
        "example_code": """
/// admonition | Some title
    type: warning

Some content
///
        """,
        "args": {
            "type": _(
                "These are Bootstrap alert levels. Possible values: note, attention, caution, danger, error, tip, hint, warning"
            ),
            "attrs": _(
                "These are attributes that are added to the admonition html tag. Example: {class: class-name: id: id-name}"
            ),
        },
    },
    {
        "short_description": _("Definition"),
        "help_text": _(
            """Insert a Definition html tag. <a href="https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/admonition/" target="_blank">Open external docs ↗</a>"""
        ),
        "example_code": """
/// define
Apple

- Pomaceous fruit of plants of the genus Malus in
  the family Rosaceae.

///

            """,
    },
    {
        "short_description": _("Details"),
        "help_text": _(
            """Insert a Details html tag. <a href="https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/admonition/" target="_blank">Open external docs ↗</a>"""
        ),
        "example_code": """
/// details | Some Summary
    Some content
///
        """,
        "args": {
            "type": _("These are Bootstrap alert levels. "),
            "attrs": _(
                "These are attributes that are added to the admonition html tag. Example: {class: class-name: id: id-name}"
            ),
            "open": _(
                "Boolean value of 'True' or 'False' to indicate that it is by default open or closed. Default False."
            ),
        },
    },
    {
        "short_description": _("HTML"),
        "help_text": _(
            """Insert a HTML html tag. NOTE: The wiki ues bleach to clean both HTML tags and certain attributes. <a href="https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/admonition/" target="_blank">Open external docs ↗</a>"""
        ),
        "example_code": """
/// html | div[style='border: 1px solid red;']
some *markdown* content
///
            """,
        "args": {
            "markdown": _(
                "String value to control how Markdown content is processed. Valid options are: auto, block, inline, html, and raw."
            ),
            "attrs": _(
                "These are attributes that are added to the admonition html tag. Example: {class: class-name: id: id-name}"
            ),
        },
    },
]
