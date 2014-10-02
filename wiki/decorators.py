# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound, \
    HttpResponseForbidden, HttpResponseRedirect

from django.shortcuts import redirect, get_object_or_404
from django.template.context import RequestContext
from django.template.loader import render_to_string
import json

from wiki.core.exceptions import NoRootURL

from wiki.conf import settings
from django.utils.http import urlquote

def json_view(func):
    def wrap(request, *args, **kwargs):
        obj = func(request, *args, **kwargs)
        if isinstance(obj, HttpResponse):
            # Special behaviour: If it's a redirect, for instance
            # because of login protection etc. just return
            # the redirect
            if obj.status_code == 301 or obj.status_code == 302:
                return obj
        data = json.dumps(obj, ensure_ascii=False)
        status = kwargs.get('status', 200)
        response = HttpResponse(mimetype='application/json', status=status)
        response.write(data)
        return response
    return wrap

def response_forbidden(request, article, urlpath):
    if request.user.is_anonymous():
        qs = request.META.get('QUERY_STRING', '')
        if qs:
            qs = urlquote('?' + qs)
        else:
            qs = ''
        return redirect(settings.LOGIN_URL+"?next="+request.path + qs)
    else:
        c = RequestContext(request, {'article': article,
                                     'urlpath' : urlpath})
        return HttpResponseForbidden(render_to_string("wiki/permission_denied.html", context_instance=c))

def get_article(func=None, can_read=True, can_write=False, 
                 deleted_contents=False, not_locked=False,
                 can_delete=False, can_moderate=False,
                 can_create=False):
    """View decorator for processing standard url keyword args: Intercepts the 
    keyword args path or article_id and looks up an article, calling the decorated 
    func with this ID.
    
    Will accept a func(request, article, *args, **kwargs)
    
    NB! This function will redirect if an article does not exist, permissions
    are missing or the article is deleted.
    
    Arguments:
    
    can_read=True and/or can_write=True: Check that the current request.user
    has correct permissions.
    
    can_delete and can_moderate: Verifies with wiki.core.permissions
    
    can_create: Same as can_write but adds an extra global setting for anonymous access (ANONYMOUS_CREATE)

    deleted_contents=True: Do not redirect if the article has been deleted.
    
    not_locked=True: Return permission denied if the article is locked
    
    Also see: wiki.views.mixins.ArticleMixin 
    """
    
    def wrapper(request, *args, **kwargs):
        from . import models

        path = kwargs.pop('path', None)
        article_id = kwargs.pop('article_id', None)
                
        urlpath = None
        
        # fetch by urlpath.path
        if not path is None:
            try:
                urlpath = models.URLPath.get_by_path(path, select_related=True)
            except NoRootURL:
                return redirect('wiki:root_create')
            except models.URLPath.DoesNotExist:
                try:
                    pathlist = list(filter(lambda x: x!="", path.split("/"),))
                    path = "/".join(pathlist[:-1])
                    parent = models.URLPath.get_by_path(path)
                    return HttpResponseRedirect(reverse("wiki:create", kwargs={'path': parent.path,}) + "?slug=%s" % pathlist[-1])
                except models.URLPath.DoesNotExist:
                    c = RequestContext(request, {'error_type' : 'ancestors_missing'})
                    return HttpResponseNotFound(render_to_string("wiki/error.html", context_instance=c))
            if urlpath.article:
                # urlpath is already smart about prefetching items on article (like current_revision), so we don't have to
                article = urlpath.article
            else:
                # Be robust: Somehow article is gone but urlpath exists... clean up
                return_url = reverse('wiki:get', kwargs={'path': urlpath.parent.path})
                urlpath.delete()
                return HttpResponseRedirect(return_url)
        
        
        # fetch by article.id
        elif article_id:
            #TODO We should try to grab the article form URLPath so the caching is good, and fall back to grabbing it from Article.objects if not
            articles = models.Article.objects
            
            article = get_object_or_404(articles, id=article_id)
            try:
                urlpath = models.URLPath.objects.get(articles__article=article)
            except models.URLPath.DoesNotExist as noarticle:
                models.URLPath.MultipleObjectsReturned = noarticle
                urlpath = None
        
        
        else:
            raise TypeError('You should specify either article_id or path')
        
        if not deleted_contents:    
            # If the article has been deleted, show a special page.        
            if urlpath:
                if urlpath.is_deleted(): # This also checks all ancestors
                    return redirect('wiki:deleted', path=urlpath.path)
            else:
                if article.current_revision and article.current_revision.deleted:
                    return redirect('wiki:deleted', article_id=article.id)
        
        
        if article.current_revision.locked and not_locked:
            return response_forbidden(request, article, urlpath)

        if can_read and not article.can_read(request.user):
            return response_forbidden(request, article, urlpath)
        
        if (can_write or can_create) and not article.can_write(request.user):
            return response_forbidden(request, article, urlpath)

        if can_create and not (request.user.is_authenticated() or settings.ANONYMOUS_CREATE):
            return response_forbidden(request, article, urlpath)
        
        if can_delete and not article.can_delete(request.user):
            return response_forbidden(request, article, urlpath)
            
        if can_moderate and not article.can_moderate(request.user):
            return response_forbidden(request, article, urlpath)
        
        kwargs['urlpath'] = urlpath
        
        return func(request, article, *args, **kwargs)
    
    if func:
        return wrapper
    else:
        return lambda func: get_article(func, can_read=can_read, can_write=can_write, 
                                        deleted_contents=deleted_contents,
                                        not_locked=not_locked,can_delete=can_delete,
                                        can_moderate=can_moderate, can_create=can_create)

