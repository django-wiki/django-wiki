# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden,\
    HttpResponseNotFound
from django.utils import simplejson as json

from wiki.core.exceptions import NoRootURL

def json_view(func):
    def wrap(request, *args, **kwargs):
        obj = func(request, *args, **kwargs)
        data = json.dumps(obj, ensure_ascii=False)
        status = kwargs.get('status', 200)
        response = HttpResponse(mimetype='application/json', status=status)
        response.write(data)
        return response
    return wrap

def get_article(func=None, can_read=True, can_write=False):
    """Intercepts the keyword args path or article_id and looks up an article,
    calling the decorated func with this ID."""
    
    def the_func(request, *args, **kwargs):
        import models

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
                    pathlist = filter(lambda x: x!="", path.split("/"),)
                    path = "/".join(pathlist[:-1])
                    parent = models.URLPath.get_by_path(path)
                    return redirect(reverse("wiki:create_url", args=(parent.path,)) + "?slug=%s" % pathlist[-1])
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

