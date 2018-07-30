"""Abstraction layer to deal with Django related changes in order to keep
compatibility with several Django versions simultaneously."""


try:
    from django.urls import include, re_path as url
except ImportError:
    from django.conf.urls import include, url


__all__ = [
    'get_default_engine',
    'include', 'url'
]


def get_default_engine():
    """
    Django >= 2.1 Engine.get_default() behaviour
    """
    from django.core.exceptions import ImproperlyConfigured
    from django.template import engines
    from django.template.backends.django import DjangoTemplates
    for engine in engines.all():
        if isinstance(engine, DjangoTemplates):
            return engine.engine
    raise ImproperlyConfigured('No DjangoTemplates backend is configured.')
