import os  # noqa @UnusedImport
import sys

from .base import *  # noqa @UnusedWildImport
from .dev import *

# Append testdata path

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(PROJECT_DIR)), "tests"))

DATABASES = {
    "default": {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        "ENGINE": "django.db.backends.sqlite3",
        # Or path to database file if using sqlite3.
        "NAME": os.path.join(PROJECT_DIR, "prepopulated-customauthuser.sqlite3"),
    }
}

INSTALLED_APPS = INSTALLED_APPS + [
    # Test application for testing custom users
    "testdata",
]

AUTH_USER_MODEL = "testdata.CustomUser"
