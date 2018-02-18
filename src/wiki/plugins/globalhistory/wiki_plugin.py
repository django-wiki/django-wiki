from wiki.compat import url
from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin

from . import settings, views


class GlobalHistoryPlugin(BasePlugin):

    slug = settings.SLUG
    urlpatterns = {'root': [
        url(r'^$', views.GlobalHistory.as_view(), name='globalhistory'),
        url('^(?P<only_last>[01])/$', views.GlobalHistory.as_view(), name='globalhistory'),
    ]}


registry.register(GlobalHistoryPlugin)
