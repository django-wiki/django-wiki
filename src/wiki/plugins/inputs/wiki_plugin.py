from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext as _
from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
from wiki.plugins.inputs import settings, views
from wiki.plugins.inputs.mdx.input import InputExtension
from django.conf.urls import url


class InputsPlugin(BasePlugin):

    slug = settings.SLUG

    urlpatterns = {'article': [
        url(r'change/(?P<input_name>.*)$', views.InputDataView.as_view(), name='input_data'),
    ]}


    sidebar = {'headline': _('Inputs'),
               'icon_class': 'fa-pencil-square-o',
               'template': 'wiki/plugins/inputs/sidebar.html',
               'form_class': None,
               'get_form_kwargs': (lambda a: {})}

    class RenderMedia:
        js = [
            'wiki/plugins/inputs/inputs.js',
            'wiki/js/jsrender.min.js',
        ]

        css = {
            'screen': 'wiki/css/inputs.css',
        }

    markdown_extensions = [InputExtension()]


registry.register(InputsPlugin)
