"""Abstraction layer to deal with Django related changes in order to keep
compatibility with several Django versions simultaneously."""
from __future__ import unicode_literals

from django.conf import settings as django_settings

USER_MODEL = getattr(django_settings, 'AUTH_USER_MODEL', 'auth.User')


# Django 1.11 Widget.build_attrs has a different signature, designed for the new
# template based rendering. The previous version was more useful for our needs,
# so we restore that version.
# When support for Django < 1.11 is dropped, we should look at using the
# new template based rendering, at which point this probably won't be needed at all.
class BuildAttrsCompat(object):
    def build_attrs_compat(self, extra_attrs=None, **kwargs):
        "Helper function for building an attribute dictionary."
        attrs = self.attrs.copy()
        if extra_attrs is not None:
            attrs.update(extra_attrs)
        if kwargs is not None:
            attrs.update(kwargs)
        return attrs


try:
    # Python 3
    from urllib.parse import urljoin  # noqa
except ImportError:
    # Python 2
    from urlparse import urljoin  # noqa @UnusedImport
