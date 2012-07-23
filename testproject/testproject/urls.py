from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from wiki.urls import get_pattern as wiki_pattern

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(wiki_pattern())),
)
