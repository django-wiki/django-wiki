# -*- coding: utf-8 -*-
from django.conf import settings as django_settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseNotFound
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

def get_article(func=None, can_read=True, can_write=False, deleted_contents=False):
    """View decorator for processing standard url keyword args: Intercepts the 
    keyword args path or article_id and looks up an article, calling the decorated 
    func with this ID.
    
    Will accept a func(request, article, *args, **kwargs)
    
    NB! This function will redirect if an article does not exist, permissions
    are missing or the article is deleted.
    
    Arguments:
    
    can_read=True and/or can_write=True: Check that the current request.user
    has correct permissions.
    
    deleted_contents=True: Do not redirect if the article has been deleted.
    
    Also see: wiki.views.mixins.ArticleMixin 
    """
    
    def wrapper(request, *args, **kwargs):
        import models

        path = kwargs.pop('path', None)
        article_id = kwargs.pop('article_id', None)
        
        articles = models.Article.objects
        
        # TODO: Is this the way to do it?
        articles = articles.select_related()
        
        urlpath = None
        if article_id:
            article = get_object_or_404(articles, id=article_id)
            try:
                urlpath = models.URLPath.objects.get(articles__article=article)
            except models.URLPath.DoesNotExist, models.URLPath.MultipleObjectsReturned:
                urlpath = None
        else:
            try:
                urlpath = models.URLPath.get_by_path(path, select_related=True)
            except NoRootURL:
                return redirect('wiki:root_create')
            except models.URLPath.DoesNotExist:
                try:
                    pathlist = filter(lambda x: x!="", path.split("/"),)
                    path = "/".join(pathlist[:-1])
                    parent = models.URLPath.get_by_path(path)
                    return redirect(reverse("wiki:create", kwargs={'path': parent.path,}) + "?slug=%s" % pathlist[-1])
                except models.URLPath.DoesNotExist:
                    # TODO: Make a nice page
                    return HttpResponseNotFound("This article was not found, and neither was the parent. This page should look nicer.")
            if urlpath.article:
                article = get_object_or_404(articles, id=urlpath.article.id)
            else:
                # Be robust: Somehow article is gone but urlpath exists... clean up
                return_url = reverse('wiki:get', kwargs={'path': urlpath.parent.path})
                urlpath.delete()
                return redirect(return_url)
        
        if can_read and not article.can_read(request.user):
            if request.user.is_anonymous():
                return redirect(django_settings.LOGIN_URL)
            else:
                c = RequestContext(request, {'urlpath' : urlpath})
                return render_to_response("wiki/permission_denied.html", context_instance=c)
                pass
        
        if can_write and not article.can_write(request.user):
            if request.user.is_anonymous():
                return redirect(django_settings.LOGIN_URL)
            else:
                c = RequestContext(request, {'urlpath' : urlpath})
                return render_to_response("wiki/permission_denied.html", context_instance=c)
                pass

        # If the article has been deleted, show a special page.
        if not deleted_contents and article.current_revision and article.current_revision.deleted:
            if urlpath:
                return redirect('wiki:deleted', path=urlpath.path)
            else:
                return redirect('wiki:deleted', article_id=article.id)
        
        kwargs['urlpath'] = urlpath
        
        return func(request, article, *args, **kwargs)
    
    if func:
        return wrapper
    else:
        return lambda func: get_article(func, can_read=can_read, can_write=can_write, 
                                        deleted_contents=deleted_contents)

