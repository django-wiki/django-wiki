"""Abstraction layer to deal with Django related changes in order to keep
compatibility with several Django versions simultaneously."""
from __future__ import absolute_import, unicode_literals

from django.conf import settings as django_settings
from django.db import transaction

USER_MODEL = getattr(django_settings, 'AUTH_USER_MODEL', 'auth.User')


def get_user_model():

    from django.contrib.auth import get_user_model as gum
    return gum()


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
