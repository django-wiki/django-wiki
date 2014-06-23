# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.utils.translation import ugettext as _

from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
from wiki.plugins.links import views
from wiki.plugins.links import settings
from wiki.plugins.links.mdx.urlize import makeExtension as urlize_makeExtension
from wiki.plugins.links.mdx.djangowikilinks import WikiPathExtension
from django.core.urlresolvers import reverse_lazy


class LinkPlugin(BasePlugin):

    slug = 'links'
    urlpatterns = {
        'article': patterns('',
            url(r'^json/query-urlpath/$', views.QueryUrlPath.as_view(), name='links_query_urlpath'),
        )
    }

    sidebar = {'headline': _('Links'),
               'icon_class': 'icon-bookmark',
               'template': 'wiki/plugins/links/sidebar.html',
               'form_class': None,
               'get_form_kwargs': (lambda a: {})}

    wikipath_config = [
        ('base_url', reverse_lazy('wiki:get', kwargs={'path': ''})),
        ('default_level', settings.LOOKUP_LEVEL),
    ]

    markdown_extensions = [urlize_makeExtension(), WikiPathExtension(wikipath_config)]

    def __init__(self):
        pass

registry.register(LinkPlugin)
