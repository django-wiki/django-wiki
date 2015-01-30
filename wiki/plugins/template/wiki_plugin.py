# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.conf.urls import patterns, url, include

from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
from wiki.plugins.template import settings
from wiki.plugins.template import models
from wiki.plugins.template import views

from wiki.plugins.template.markdown_extensions import TemplateExtension

from wiki.plugins.notifications.settings import ARTICLE_EDIT
from wiki.plugins.notifications.util import truncate_title


class TemplatePlugin(BasePlugin):

    slug = settings.SLUG
    sidebar = {'headline': _('Template'),
               'icon_class': 'fa fa-file-text-o',
               'template': 'wiki/plugins/template/sidebar.html',
               'form_class': None,
               'get_form_kwargs': (lambda a: {})}
    urlpatterns = {
        'article': patterns('',
            url('', include('wiki.plugins.template.urls')),
        )
    }

    article_tab = (_('Template'), "fa fa-file-text-o")
    article_view = views.TemplateView().dispatch

    # List of notifications to construct signal handlers for. This
    # is handled inside the notifications plugin.
    notifications = [{
        'model': models.TemplateRevision,
        'message': lambda obj: _("A tempalte was changed: %s") % truncate_title(obj.template.template_title),
        'key': ARTICLE_EDIT,
        'created': True,
        'get_article': lambda obj: obj.template.article}
    ]

    markdown_extensions = [TemplateExtension(), ]

    def __init__(self):
        pass

registry.register(TemplatePlugin)
