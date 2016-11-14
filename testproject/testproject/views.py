from django.conf import settings
from django.http import HttpResponseServerError
from django.template import loader
from django.template.context import RequestContext
from django.views.decorators.csrf import requires_csrf_token


@requires_csrf_token
def server_error(request, template_name='500.html', **param_dict):
    # You need to create a 500.html template.
    t = loader.get_template(template_name)
    return HttpResponseServerError(t.render(RequestContext(
        request,
        {
            'MEDIA_URL': settings.MEDIA_URL,
            'STATIC_URL': settings.STATIC_URL,
            'request': request,
        },
    )))


def page_not_found(request, template_name='404.html', exception=None):
    response = server_error(
        request,
        template_name=template_name,
        exception=exception
    )
    response.status_code = 404
    return response
