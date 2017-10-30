from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http.response import HttpResponse
from django.views.static import serve as static_serve
from django_nyt.urls import get_pattern as get_notify_pattern
from wiki.urls import get_pattern as get_wiki_pattern
from testproject.views import martor
from testproject.views import simplemde
from wiki.views import article

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots.txt', lambda _: HttpResponse('User-agent: *\nDisallow: /')),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT}),
    ]


urlpatterns += [
    url(r'^martor/(?P<path>.+/|)_create/$', martor.as_view()),
    url(r'^simplemde/(?P<path>.+/|)_create/$', simplemde.as_view()),
    url(r'^notify/', get_notify_pattern()),
    url(r'', get_wiki_pattern())
]

handler500 = 'testproject.views.server_error'
handler404 = 'testproject.views.page_not_found'
