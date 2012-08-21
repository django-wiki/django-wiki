# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.utils.translation import ugettext as _

from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
from wiki.plugins.images import views, models, settings, forms
from wiki.plugins.notifications import ARTICLE_EDIT
from wiki.plugins.images.markdown_extensions import ImageExtension

class ImagePlugin(BasePlugin):
    
    slug = settings.SLUG
    sidebar = {
        'headline': _('Images'),
        'icon_class': 'icon-picture',
        'template': 'wiki/plugins/images/sidebar.html',
        'form_class': forms.SidebarForm,
        'get_form_kwargs': (lambda a: {'instance': models.Image(article=a)})
    }
    
    # List of notifications to construct signal handlers for. This
    # is handled inside the notifications plugin.
    notifications = [
        {'model': models.ImageRevision,
         'message': lambda obj: _(u"An image was added: %s") % obj.get_filename(),
         'key': ARTICLE_EDIT,
         'created': False,
         'ignore': lambda revision: bool(revision.previous_revision), # Ignore if there is a previous revision... the image isn't new
         'get_article': lambda obj: obj.article}
    ]
    
    class RenderMedia:
        js = [
            'wiki/colorbox/colorbox/jquery.colorbox-min.js',
            'wiki/js/images.js',
        ]
        
        css = {
            'screen': 'wiki/colorbox/example1/colorbox.css'
        }
    
    urlpatterns = patterns('',
        url('^$', views.ImageView.as_view(), name='images_index'),
        url('^delete/(?P<image_id>\d+)/$', views.DeleteView.as_view(), name='images_delete'),
        url('^restore/(?P<image_id>\d+)/$', views.DeleteView.as_view(), name='images_restore', kwargs={'restore': True}),
        url('^purge/(?P<image_id>\d+)/$', views.PurgeView.as_view(), name='images_purge'),
        url('^(?P<image_id>\d+)/revision/change/(?P<rev_id>\d+)/$', views.RevisionChangeView.as_view(), name='images_restore'),
        url('^(?P<image_id>\d+)/revision/add/$', views.RevisionAddView.as_view(), name='images_add_revision'),
    )

    markdown_extensions = [ImageExtension()]
    
    def __init__(self):
        #print "I WAS LOADED!"
        pass
    
registry.register(ImagePlugin)

