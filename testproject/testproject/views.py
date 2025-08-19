from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token


@requires_csrf_token
def server_error(request, template_name="500.html", **param_dict):
    return render(
        request,
        template_name,
        context={
            "MEDIA_URL": settings.MEDIA_URL,
            "STATIC_URL": settings.STATIC_URL,
            "request": request,
        },
        status=500,
    )


def page_not_found(request, template_name="404.html", exception=None):
    response = server_error(request, template_name=template_name, exception=exception)
    response.status_code = 404
    return response
