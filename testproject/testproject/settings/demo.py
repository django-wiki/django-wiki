from .base import *  # noqa

DEBUG = False

ALLOWED_HOSTS = [".demo.django-wiki.org"]
SESSION_COOKIE_DOMAIN = ".demo.django-wiki.org"
SESSION_COOKIE_SECURE = True

MIDDLEWARE += ["testproject.middleware.DemoMiddleware"]
