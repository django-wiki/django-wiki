from .base import *  # noqa @UnusedWildImport
from .demo import *  # noqa @UnusedWildImport

DEBUG = True

for template_engine in TEMPLATES:
    template_engine["OPTIONS"]["debug"] = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Used by debug_toolbar
INTERNAL_IPS = ["127.0.0.1"]

ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
]

# Removed.
# See: https://forum.djangoproject.com/t/why-are-cookie-secure-settings-defaulted-to-false/1133/4
# and https://github.com/django-wiki/django-wiki/pull/1325
# SESSION_COOKIE_DOMAIN = ".localhost"
SESSION_COOKIE_SECURE = False

try:
    import debug_toolbar  # @UnusedImport

    MIDDLEWARE = list(MIDDLEWARE) + [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    INSTALLED_APPS = list(INSTALLED_APPS) + ["debug_toolbar"]
    DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False}
except ImportError:
    pass
