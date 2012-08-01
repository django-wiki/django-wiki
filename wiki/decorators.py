from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseForbidden,\
    HttpResponseNotFound

import models
from wiki.core.exceptions import NoRootURL
from django.shortcuts import redirect, get_object_or_404

def json_view(func):
    def wrap(request, *a, **kw):
        obj = func(request, *a, **kw)
        data = json.dumps(obj, ensure_ascii=False)
        response = HttpResponse(mimetype='application/json')
        response.write(data)
        return response
    return wrap

def get_article(func=None, can_read=True, can_write=False):
    """Intercepts the keyword args path or article_id and looks up an article,
    calling the decorated func with this ID."""
    
    def the_func(request, *args, **kwargs):

        path = kwargs.pop('path', None)
        article_id = kwargs.pop('article_id', None)
        
        urlpath = None
        if not path is None:
            try:
                urlpath = models.URLPath.get_by_path(path)
            except NoRootURL:
                return redirect('wiki:root_create')
            except models.URLPath.DoesNotExist:
                try:
                    path = "/".join(filter(lambda x: x!="", path.split("/"),)[:-1])
                    parent = models.URLPath.get_by_path(path)
                    return redirect("wiki:create_url", parent.path)
                except models.URLPath.DoesNotExist:
                    return HttpResponseNotFound("This article was not found. This page should look nicer.")
            article = urlpath.article
        elif article_id:
            article = get_object_or_404(models.Article, id=article_id)
        
        if not article.can_write(request.user):
            raise HttpResponseForbidden()
        
        kwargs['urlpath'] = urlpath
        
        return func(request, article, *args, **kwargs)
    
    if func:
        return the_func
    else:
        return lambda func: get_article(func, can_read=can_read, can_write=can_write)

