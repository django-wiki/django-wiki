from __future__ import absolute_import
from __future__ import unicode_literals
from testproject.settings import *
from testproject.settings.local import *

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',
        # Or path to database file if using sqlite3.
        'NAME': os_path.join(PROJECT_PATH, 'db', 'prepopulated-customauthuser.db'),
    }
}

INSTALLED_APPS = INSTALLED_APPS + [
    # Test application for testing custom users
    'wiki.tests.testdata',
]

AUTH_USER_MODEL = 'testdata.CustomUser'
