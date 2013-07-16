# -*- coding: utf-8 -*-
from django.utils.importlib import import_module

def get_class_from_str(class_path):
    """Dynamically load a View class from a string path
    "myapp.views.MyView" -- used for dynamic settings"""
    module_path, klass_name = class_path.rsplit('.', 1)
    module = import_module(module_path)
    return getattr(module, klass_name)        
    
