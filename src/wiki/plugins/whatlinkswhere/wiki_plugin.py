from django.urls import re_path
from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin

from . import settings
from . import views


class WhatLinksWherePlugin(BasePlugin):
    slug = settings.SLUG

    urlpatterns = {
        "article": [
            re_path(r"^$", views.WhatLinksHere.as_view(), name="whatlinkshere"),
            re_path(
                r"^network/$", views.WhatLinksWhere.as_view(), name="whatlinkswhere"
            ),
        ]
    }


registry.register(WhatLinksWherePlugin)