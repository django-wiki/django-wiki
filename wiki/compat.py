from django.db import transaction

# Django 1.6 transaction API, required for 1.8+

def nop_decorator(func):
    return func

# Where these are used in code, both old and new methods for transactions appear
# to be used, but only one will actually do anything. When only Django 1.8+
# is supported, transaction_commit_on_success can be deleted.
try:
    atomic = transaction.atomic # Does it exist?
    transaction_commit_on_success = nop_decorator
except AttributeError:
    atomic = nop_decorator
    transaction_commit_on_success = transaction.commit_on_success
