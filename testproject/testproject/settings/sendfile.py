from .base import *  # noqa @UnusedWildImport

INSTALLED_APPS += ['sendfile']

WIKI_ATTACHMENTS_USE_SENDFILE = True


SENDFILE_BACKEND = 'sendfile.backends.development'
# SENDFILE_URL = None #Not needed
# SENDFILE_ROOT = None #Not needed
