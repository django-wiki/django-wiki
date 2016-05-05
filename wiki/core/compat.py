"""Abstraction layer to deal with Django related changes in order to keep
compatibility with several Django versions simultaneously."""
from __future__ import absolute_import, unicode_literals

from django import VERSION as DJANGO_VERSION
from django.conf import settings as django_settings
from django.db import transaction

# Django 1.5+
if DJANGO_VERSION >= (1, 5):
    USER_MODEL = getattr(django_settings, 'AUTH_USER_MODEL', 'auth.User')
else:
    USER_MODEL = 'auth.User'


def get_user_model():

    if DJANGO_VERSION >= (1, 5):
        from django.contrib.auth import get_user_model as gum
        return gum()
    else:
        from django.contrib.auth.models import User
        if 'USERNAME_FIELD' not in User.__dict__:
            User.USERNAME_FIELD = 'username'
        return User


# Django 1.6 transaction API, required for 1.8+
def nop_decorator(func):
    return func

# Where these are used in code, both old and new methods for transactions appear
# to be used, but only one will actually do anything. When only Django 1.8+
# is supported, transaction_commit_on_success can be deleted.
try:
    atomic = transaction.atomic  # Does it exist?
    transaction_commit_on_success = nop_decorator
except AttributeError:
    atomic = nop_decorator
    transaction_commit_on_success = transaction.commit_on_success


if DJANGO_VERSION < (1, 8):
    from django.template.loader import render_to_string as django_render_to_string
    from django.template import Context, RequestContext

    # Similar to 1.8 signature, but with things we can support
    # under 1.7 and less.
    def render_to_string(template_name, context=None, request=None):
        if request is not None:
            context_instance = RequestContext(request, context)
        else:
            context_instance = Context(context)
        return django_render_to_string(template_name,
                                       context_instance=context_instance)
else:
    from django.template.loader import render_to_string  # noqa @UnusedImport
