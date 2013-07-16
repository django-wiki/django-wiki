from testproject.settings import *
from testproject.settings.local import *
import os

#Django Haystack

HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_PATH, 'index_woosh')

INSTALLED_APPS += ['haystack', 'wiki.plugins.haystack']

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PROJECT_PATH, 'whoosh_index'),
    },
}
