from .base import *  # noqa

DEBUG = False

INTERNAL_IPS = []
ALLOWED_HOSTS = ["django-wiki.org"]
SESSION_COOKIE_DOMAIN = ".django-wiki.org"
SESSION_COOKIE_SECURE = True

MIDDLEWARE += ["testproject.middleware.DemoMiddleware"]
