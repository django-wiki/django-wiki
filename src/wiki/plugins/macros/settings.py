from django.conf import settings as django_settings

SLUG = "macros"
APP_LABEL = "wiki"

#: List of markdown extensions this plugin should support.
#: ``article_list`` inserts a list of articles from the current level.
#: ``toc`` inserts a table of contents matching the headings.
METHODS = getattr(
    django_settings,
    "WIKI_PLUGINS_METHODS",
    (
        "article_list",
        "toc",
    ),
)
