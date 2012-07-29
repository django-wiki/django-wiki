# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseForbidden
from django.utils.translation import ugettext as _

import models
import forms
import editors
from wiki.core.exceptions import NoRootURL
from django.contrib import messages
from django.views.generic.list import ListView

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

@get_article(can_read=True)
def preview(request, article, urlpath=None, template_file="wiki/preview_inline.html"):
    
    content = article.current_revision.content
    title = article.current_revision.title
    
    if request.method == 'POST':
        edit_form = forms.EditForm(article.current_revision, request.POST, preview=True)
        if edit_form.is_valid():
            title = edit_form.cleaned_data['title']
            content = edit_form.cleaned_data['content']
    
    c = RequestContext(request, {'urlpath': urlpath,
                                 'article': article,
                                 'title': title,
                                 'content': content})
    return render_to_response(template_file, c)

@get_article(can_read=True)
def root(request, article, template_file="wiki/article.html", urlpath=None):
    
    c = RequestContext(request, {'urlpath': urlpath,
                                 'article': article,})
    return render_to_response(template_file, c)

@get_article(can_write=True)
def edit(request, article, template_file="wiki/edit.html", urlpath=None):
    
    if request.method == 'POST':
        edit_form = forms.EditForm(article.current_revision, request.POST)
        if edit_form.is_valid():
            revision = models.ArticleRevision()
            revision.inherit_predecessor(article)
            revision.title = edit_form.cleaned_data['title']
            revision.content = edit_form.cleaned_data['content']
            article.add_revision(revision)
            messages.success(request, _(u'A new revision of the article was succesfully added.'))
            if not urlpath is None:
                return redirect("wiki:get_url", urlpath.path)
            # TODO: Where to go if it's a different object? It's probably
            # an ajax callback, so we don't care... but should perhaps return
            # a status
            return
    else:
        edit_form = forms.EditForm(article.current_revision)
    
    c = RequestContext(request, {'article': article,
                                 'urlpath': urlpath,
                                 'edit_form': edit_form,
                                 'editor': editors.editor})
    return render_to_response(template_file, c)

@get_article(can_read=True)
def history(request, article, template_file="wiki/history.html", urlpath=None):
    
    c = RequestContext(request, {'article': article,
                                 'urlpath': urlpath,})
    return render_to_response(template_file, c)
    
@permission_required('wiki.add_article')
def root_create(request):
    if request.method == 'POST':
        create_form = forms.CreateRoot(request.POST)
        if create_form.is_valid():
            root = models.URLPath.create_root(title=create_form.cleaned_data["title"],
                                              content=create_form.cleaned_data["content"])
            return redirect("wiki:root")
    else:
        create_form = forms.CreateRoot()
    
    c = RequestContext(request, {'create_form': create_form,
                                 'editor': editors.editor,})
    return render_to_response("wiki/article/create_root.html", c)

def get_url(request, path):
    
    path = models.URLPath.get_by_path(path)
