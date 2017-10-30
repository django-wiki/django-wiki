from django.conf import settings
from django.http import HttpResponseServerError
from django.template import loader
from django.template.context import RequestContext
from django.views.decorators.csrf import requires_csrf_token
from wiki.views import article
from wiki import editors, forms, models
from wiki.editors import _editor, _EditorClass
from wiki.editors import getEditor


class martor(article.Create):

    def get_form(self, form_class=None):
        editors._editor = None
        editors._EditorClass = None 
        settings.WIKI_EDITOR = 'wiki.editors.martor.Martor'
        settings.EDITOR = settings.WIKI_EDITOR
        editors.getEditor()
        return super(martor, self).get_form(form_class)

class simplemde(article.Create):

    form_class = forms.CreateForm
    template_name = "wiki/create.html"
    def get_form(self, form_class=None):
        _EditorClass = None
        _editor = None
        WIKI_EDITOR = 'wiki.editors.simplemde.SimpleMDE'
        EDITOR = WIKI_EDITOR
        getEditor()
        return super(simplemde, self).get_form(form_class=form_class)


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
