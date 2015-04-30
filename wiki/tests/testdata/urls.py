from __future__ import absolute_import
from __future__ import unicode_literals
from django import VERSION as DJANGO_VERSION
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT,
             }),
    ]

from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_notify_pattern
urlpatterns += [
    url(r'^notify/', get_notify_pattern()),
    url(r'', get_wiki_pattern())
]

if DJANGO_VERSION < (1, 8):
    urlpatterns = patterns('', *urlpatterns)