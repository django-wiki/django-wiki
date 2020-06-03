from django.urls import re_path
from django.utils.translation import gettext as _
from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
from wiki.plugins.images import forms
from wiki.plugins.images import models
from wiki.plugins.images import settings
from wiki.plugins.images import views
from wiki.plugins.images.markdown_extensions import ImageExtension
from wiki.plugins.notifications.settings import ARTICLE_EDIT
from wiki.plugins.notifications.util import truncate_title


class ImagePlugin(BasePlugin):

    slug = settings.SLUG
    sidebar = {
        "headline": _("Images"),
        "icon_class": "fa-image",
        "template": "wiki/plugins/images/sidebar.html",
        "form_class": forms.SidebarForm,
        "get_form_kwargs": (lambda a: {"instance": models.Image(article=a)}),
    }

    # List of notifications to construct signal handlers for. This
    # is handled inside the notifications plugin.
    notifications = [
        {
            "model": models.ImageRevision,
            "message": lambda obj: _("An image was added: %s")
            % truncate_title(obj.get_filename()),
            "key": ARTICLE_EDIT,
            "created": False,
            # Ignore if there is a previous revision... the image isn't new
            "ignore": lambda revision: bool(revision.previous_revision),
            "get_article": lambda obj: obj.article,
        }
    ]

    class RenderMedia:
        js = [
            "wiki/colorbox/jquery.colorbox-min.js",
            "wiki/js/images.js",
        ]

        css = {"screen": "wiki/colorbox/example1/colorbox.css"}

    urlpatterns = {
        "article": [
            re_path("^$", views.ImageView.as_view(), name="images_index"),
            re_path(
                "^delete/(?P<image_id>[0-9]+)/$",
                views.DeleteView.as_view(),
                name="images_delete",
            ),
            re_path(
                "^restore/(?P<image_id>[0-9]+)/$",
                views.DeleteView.as_view(),
                name="images_restore",
                kwargs={"restore": True},
            ),
            re_path(
                "^purge/(?P<image_id>[0-9]+)/$",
                views.PurgeView.as_view(),
                name="images_purge",
            ),
            re_path(
                "^(?P<image_id>[0-9]+)/revision/change/(?P<rev_id>[0-9]+)/$",
                views.RevisionChangeView.as_view(),
                name="images_set_revision",
            ),
            re_path(
                "^(?P<image_id>[0-9]+)/revision/add/$",
                views.RevisionAddView.as_view(),
                name="images_add_revision",
            ),
        ]
    }

    markdown_extensions = [ImageExtension()]


registry.register(ImagePlugin)
