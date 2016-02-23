import threading
import importlib

from django.conf import settings

if getattr(settings, "WIKI_REQUEST_CACHE_MIDDLEWARE_CLASS", None):
    class_name = settings.WIKI_REQUEST_CACHE_MIDDLEWARE_CLASS.split(".")[-1]
    module = ".".join(settings.WIKI_REQUEST_CACHE_MIDDLEWARE_CLASS.split('.')[:-1])
    RequestCache = getattr(importlib.import_module(module), class_name)
else:
    class _RequestCache(threading.local):
        """
        A thread-local for storing the per-request cache.
        """
        def __init__(self):
            super(_RequestCache, self).__init__()
            self.data = {}
            self.request = None


    REQUEST_CACHE = _RequestCache()


    class RequestCache(object):
        @classmethod
        def get_request_cache(cls, name=None):
            """
            This method is deprecated. Please use :func:`request_cache.get_cache`.
            """
            if name is None:
                return REQUEST_CACHE
            else:
                return REQUEST_CACHE.data.setdefault(name, {})

        @classmethod
        def get_current_request(cls):
            """
            This method is deprecated. Please use :func:`request_cache.get_request`.
            """
            return REQUEST_CACHE.request

        @classmethod
        def clear_request_cache(cls):
            """
            Empty the request cache.
            """
            REQUEST_CACHE.data = {}
            REQUEST_CACHE.request = None

        def process_request(self, request):
            self.clear_request_cache()
            REQUEST_CACHE.request = request
            return None

        def process_response(self, request, response):
            self.clear_request_cache()
            return response


def get_current_request():
    """Return the request associated with the current thread."""
    return RequestCache.get_current_request()
