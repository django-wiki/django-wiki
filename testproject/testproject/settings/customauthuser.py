from testproject.settings import *
from testproject.settings.local import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os_path.join(PROJECT_PATH, 'db', 'prepopulated-customauthuser.db'),                      # Or path to database file if using sqlite3.
    }
}

INSTALLED_APPS = INSTALLED_APPS + [
    # Test application for testing custom users
    'wiki.tests.testdata',
]

AUTH_USER_MODEL = 'testdata.CustomUser'