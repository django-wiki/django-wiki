from django.urls import re_path
from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin

from . import settings, views


class GlobalHistoryPlugin(BasePlugin):

    slug = settings.SLUG
    urlpatterns = {
        "root": [
            re_path(r"^$", views.GlobalHistory.as_view(), name="globalhistory"),
            re_path(
                "^(?P<only_last>[01])/$",
                views.GlobalHistory.as_view(),
                name="globalhistory",
            ),
        ]
    }


registry.register(GlobalHistoryPlugin)
