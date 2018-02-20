"""Abstraction layer to deal with Django related changes in order to keep
compatibility with several Django versions simultaneously."""


try:
    from django.urls import include, re_path as url
except ImportError:
    from django.conf.urls import include, url


__all__ = [
    'BuildAttrsCompat',
    'get_default_engine',
    'include', 'url'
]


# Django 1.11 Widget.build_attrs has a different signature, designed for the new
# template based rendering. The previous version was more useful for our needs,
# so we restore that version.
# When support for Django < 1.11 is dropped, we should look at using the
# new template based rendering, at which point this probably won't be needed at all.
class BuildAttrsCompat:
    def build_attrs_compat(self, extra_attrs=None, **kwargs):
        "Helper function for building an attribute dictionary."
        attrs = self.attrs.copy()
        if extra_attrs is not None:
            attrs.update(extra_attrs)
        if kwargs is not None:
            attrs.update(kwargs)
        return attrs


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
