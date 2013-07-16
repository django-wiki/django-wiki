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
        'ENGINE': 'xapian_backend.XapianEngine',
        'PATH': os.path.join(PROJECT_PATH, 'xapian_index'),
    },
}

# Whoosh backend is completely broken
# https://github.com/toastdriven/django-haystack/issues/522
# https://github.com/toastdriven/django-haystack/issues/382
# https://github.com/toastdriven/django-haystack/issues/447
#HAYSTACK_CONNECTIONS = {
#    'default': {
#        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
#        'PATH': os.path.join(PROJECT_PATH, 'whoosh_index'),
#    },
#}
