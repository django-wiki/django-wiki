# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.utils.translation import ugettext as _
from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
from wiki.plugins.images import forms, models, settings, views
from wiki.plugins.images.markdown_extensions import ImageExtension
from wiki.plugins.notifications.settings import ARTICLE_EDIT
from wiki.plugins.notifications.util import truncate_title


class ImagePlugin(BasePlugin):

    slug = settings.SLUG
    sidebar = {
        'headline': _('Images'),
        'icon_class': 'fa-picture-o',
        'template': 'wiki/plugins/images/sidebar.html',
        'form_class': forms.SidebarForm,
        'get_form_kwargs': (lambda a: {'instance': models.Image(article=a)})
    }

    # List of notifications to construct signal handlers for. This
    # is handled inside the notifications plugin.
    notifications = [
        {'model': models.ImageRevision,
         'message': lambda obj: _("An image was added: %s") % truncate_title(obj.get_filename()),
         'key': ARTICLE_EDIT,
         'created': False,
         # Ignore if there is a previous revision... the image isn't new
         'ignore': lambda revision: bool(revision.previous_revision),
         'get_article': lambda obj: obj.article}
    ]

    class RenderMedia:
        js = [
            'wiki/colorbox/jquery.colorbox-min.js',
            'wiki/js/images.js',
        ]

        css = {
            'screen': 'wiki/colorbox/example1/colorbox.css'
        }

    urlpatterns = {'article': [
        url('^$',
            views.ImageView.as_view(),
            name='images_index'),
        url('^delete/(?P<image_id>\d+)/$',
            views.DeleteView.as_view(),
            name='images_delete'),
        url('^restore/(?P<image_id>\d+)/$',
            views.DeleteView.as_view(),
            name='images_restore',
            kwargs={'restore': True}),
        url('^purge/(?P<image_id>\d+)/$',
            views.PurgeView.as_view(),
            name='images_purge'),
        url('^(?P<image_id>\d+)/revision/change/(?P<rev_id>\d+)/$',
            views.RevisionChangeView.as_view(),
            name='images_set_revision'),
        url('^(?P<image_id>\d+)/revision/add/$',
            views.RevisionAddView.as_view(),
            name='images_add_revision'),
    ]}

    markdown_extensions = [ImageExtension()]

    def __init__(self):
        # print "I WAS LOADED!"
        pass

registry.register(ImagePlugin)
