from testproject.settings import *
from testproject.settings.local import *

#Django Haystack

INSTALLED_APPS += ['sendfile']

WIKI_ATTACHMENTS_USE_SENDFILE = True


SENDFILE_BACKEND = 'sendfile.backends.development'
#SENDFILE_URL = '/protected'

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
