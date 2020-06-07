from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http.response import HttpResponse
from django.urls import include
from django.urls import re_path
from django.views.static import serve as static_serve

admin.autodiscover()

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^robots.txt", lambda _: HttpResponse("User-agent: *\nDisallow: /")),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            static_serve,
            {"document_root": settings.MEDIA_ROOT},
        ),
    ]

if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns = [
            re_path("__debug__/", include(debug_toolbar.urls)),
            # For django versions before 2.0:
            # url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass

urlpatterns += [
    re_path(r"^notify/", include("django_nyt.urls")),
    re_path(r"", include("wiki.urls")),
]

handler500 = "testproject.views.server_error"
handler404 = "testproject.views.page_not_found"
