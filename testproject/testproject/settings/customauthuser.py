import os  # noqa @UnusedImport

from .base import *  # noqa @UnusedWildImport

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',
        # Or path to database file if using sqlite3.
        'NAME': os.path.join(PROJECT_DIR, 'db', 'prepopulated-customauthuser.db'),
    }
}

INSTALLED_APPS = PROJECT_DIR + [
    # Test application for testing custom users
    'wiki.tests.testdata',
]

AUTH_USER_MODEL = 'testdata.CustomUser'
