# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib.auth.decorators import permission_required

import models
import forms
from conf import settings
from wiki.core.exceptions import NoRootURL
from django.core.urlresolvers import get_callable

def root(request):
    
    try:
        urlpath = models.URLPath.root()
    except NoRootURL:
        return redirect('wiki:root_create')
    
    c = RequestContext(request, {'urlpath': urlpath})
    return render_to_response("wiki/article.html", c)

@permission_required('wiki.add_article')
def root_create(request):
    if request.method == 'POST':
        create_form = forms.CreateRoot(request.POST)
        if create_form.is_valid():
            root = models.URLPath.create_root()
            return redirect("wiki:root")
    else:
        create_form = forms.CreateRoot()
    
    # Insert current editor
    EditorClass = get_callable(settings.EDITOR)
    editor = EditorClass()
    create_form.fields['content'].widget = editor.get_widget()
    
    c = RequestContext(request, {'create_form': create_form,
                                 'editor': editor,})
    return render_to_response("wiki/article/create_root.html", c)

def get_url(request, path):
    
    path = models.URLPath.get_by_path(path)
