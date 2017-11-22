from __future__ import unicode_literals

from django.utils.translation import ugettext as _


def get_title(article):
    """Utility function to format the title of an article..."""
    return truncate_title(article.title)


def truncate_title(title):
    """Truncate a title (of an article, file, image etc) to be displayed in notifications messages."""
    if not title:
        return _("(none)")
    if len(title) > 25:
        return "%s..." % title[:22]
    return title
