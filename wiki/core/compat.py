"""Abstraction layer to deal with Django related changes in order to keep
compatibility with several Django versions simultaneously."""
from django import VERSION as DJANGO_VERSION

def get_user_model():
    
    if DJANGO_VERSION >= (1,5):
        from django.contrib.auth import get_user_model as gum
        return gum()
    else:
        from django.contrib.auth.models import User
        return User
