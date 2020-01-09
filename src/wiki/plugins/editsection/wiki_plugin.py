from django.conf.urls import url
from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
from wiki.plugins.editsection.markdown_extensions import EditSectionExtension

from . import settings, views


class EditSectionPlugin(BasePlugin):

    slug = settings.SLUG
    urlpatterns = {
        "article": [
            url(
                r"^(?P<location>[0-9-]+)/header/(?P<header>\w+)/$",
                views.EditSection.as_view(),
                name="editsection",
            ),
        ]
    }

    markdown_extensions = [EditSectionExtension()]


registry.register(EditSectionPlugin)
