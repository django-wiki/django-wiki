# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from importlib import import_module

from django.http.response import JsonResponse


def get_class_from_str(class_path):
    """Dynamically load a View class from a string path
    "myapp.views.MyView" -- used for dynamic settings"""
    module_path, klass_name = class_path.rsplit('.', 1)
    module = import_module(module_path)
    return getattr(module, klass_name)


def object_to_json_response(obj, status=200):
    """
    Given an object, returns an HttpResponse object with a JSON serialized
    version of that object
    """
    return JsonResponse(
        data=obj, status=status, safe=False, json_dumps_params={'ensure_ascii': False},
    )
