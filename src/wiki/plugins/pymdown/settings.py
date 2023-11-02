from django.conf import settings as django_settings
from wiki.conf import settings


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
