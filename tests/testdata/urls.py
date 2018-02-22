from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from wiki.compat import include, url
from wiki.urls import get_pattern as get_wiki_pattern

admin.autodiscover()

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT,
             }),
    ]

urlpatterns += [
    url(r'^django_functest/', include('django_functest.urls')),
    url(r'^notify/', include('django_nyt.urls')),
    url(r'', get_wiki_pattern())
]
