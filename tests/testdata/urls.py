from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include
from django.urls import re_path

urlpatterns = [
    re_path(r"^admin/doc/", include("django.contrib.admindocs.urls")),
    re_path(r"^admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            "django.views.static.serve",
            {"document_root": settings.MEDIA_ROOT},
        ),
    ]

urlpatterns += [
    re_path(r"^django_functest/", include("django_functest.urls")),
    re_path(r"^notify/", include("django_nyt.urls")),
    re_path(r"", include("wiki.urls")),
]
