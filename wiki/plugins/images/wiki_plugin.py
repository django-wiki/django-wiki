# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.utils.translation import ugettext as _

from wiki.core import plugins_registry
from wiki import plugins
from wiki.plugins.images import views, models, settings, forms
from wiki.plugins.notifications import ARTICLE_EDIT

class ImagePlugin(plugins.BasePlugin):
    
    #settings_form = 'wiki.plugins.notifications.forms.SubscriptionForm'
    
    slug = settings.SLUG
    urlpatterns = patterns('',
        url('^$', views.ImageView.as_view(), name='images_index'),
    )
    
    sidebar = {'headline': _('Images'),
               'icon_class': 'icon-picture',
               'template': 'wiki/plugins/images/sidebar.html',
               'form_class': forms.SidebarForm,
               'get_form_kwargs': (lambda a: {'instance': models.Image(article=a)})}
    
    # List of notifications to construct signal handlers for. This
    # is handled inside the notifications plugin.
    notifications = [{'model': models.Image,
                      'message': lambda obj: _(u"An image was added: %s") % obj.get_filename(),
                      'key': ARTICLE_EDIT,
                      'created': True,
                      'get_article': lambda obj: obj.article}
                     ]
    
    urlpatterns = patterns('',
        url('^$', views.ImageView.as_view(), name='images_index'),
    )

    #markdown_extensions = [AttachmentExtension()]
    
    def __init__(self):
        #print "I WAS LOADED!"
        pass
    
plugins_registry.register(ImagePlugin)

