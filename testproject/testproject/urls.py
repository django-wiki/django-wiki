from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http.response import HttpResponse
from django.views.static import serve as static_serve
from django.urls import include, re_path

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


urlpatterns += [
    re_path(r"^notify/", include("django_nyt.urls")),
    re_path(r"", include("wiki.urls")),
]

handler500 = "testproject.views.server_error"
handler404 = "testproject.views.page_not_found"
