from django import VERSION

# This is deprecated in django 1.7+
APP_LABEL = 'notifications' if VERSION < (1, 7) else None

# Key for django_nyt - changing it will break any existing notifications.
ARTICLE_EDIT = "article_edit"

SLUG = 'notifications'