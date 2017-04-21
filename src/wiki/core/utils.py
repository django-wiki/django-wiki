# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
from importlib import import_module

from django.http.response import HttpResponse


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
    data = json.dumps(obj, ensure_ascii=False)
    response = HttpResponse(content_type='application/json', status=status)
    response.write(data)
    return response
