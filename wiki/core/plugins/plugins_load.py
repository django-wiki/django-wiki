# -*- coding: utf-8 -*-
"""
Credits to ojii, functions get_module and load are from:
https://github.com/ojii/django-load.

Thanks for the technique!
"""
from django.conf import settings
from django.utils.importlib import import_module

def get_module(app, modname, verbose, failfast):
    """
    Internal function to load a module from a single app.
    """
    module_name = '%s.%s' % (app, modname)
    try:
        module = import_module(module_name)
    except ImportError, e:
        if failfast:
            raise e
        elif verbose:
            print "Could not load %r from %r: %s" % (modname, app, e)
        return None
    if verbose:
        print "Loaded %r from %r" % (modname, app)
    return module

def load(modname, verbose=False, failfast=False):
    """
    Loads all modules with name 'modname' from all installed apps.
    If verbose is True, debug information will be printed to stdout.
    If failfast is True, import errors will not be surpressed.
    """
    for app in settings.INSTALLED_APPS:
        get_module(app, modname, verbose, failfast)

def load_wiki_plugins():
    load('wiki_plugin', verbose=False)
