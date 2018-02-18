from .base import *  # noqa @UnusedWildImport

DEBUG = True


for template_engine in TEMPLATES:
    template_engine['OPTIONS']['debug'] = True


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    import debug_toolbar  # @UnusedImport
    MIDDLEWARE = list(MIDDLEWARE) + [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
    INSTALLED_APPS = list(INSTALLED_APPS) + ['debug_toolbar']
    INTERNAL_IPS = ('127.0.0.1',)
    DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
except ImportError:
    pass
