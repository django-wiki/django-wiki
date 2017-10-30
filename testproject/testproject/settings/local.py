# Add your own changes here -- but do not push to remote!!
# After changing the file, from root of repository execute:

# git update-index --assume-unchanged testproject/testproject/settings/local.py
import time
from .dev import *  # noqa @UnusedWildImport


# WIKI_EDITOR = 'wiki.editors.simplemde.SimpleMDE'
WIKI_EDITOR = 'wiki.editors.martor.Martor'

INSTALLED_APPS = list(INSTALLED_APPS) + ['simplemde']
INSTALLED_APPS = list(INSTALLED_APPS) + ['martor']

ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1']

TEMPLATE_DEBUG = True
CSRF_COOKIE_HTTPONLY = False

MARTOR_ENABLE_CONFIGS = {
    'imgur': 'true',     # to enable/disable imgur uploader/custom uploader.
    'mention': 'true',   # to enable/disable mention
    'jquery': 'false',    # to include/revoke jquery (require for admin default django)
}
MARTOR_UPLOAD_PATH = 'images/uploads/{}'.format(time.strftime("%Y/%m/%d/"))
MARTOR_UPLOAD_URL = '/api/uploader/'  # change to local uploader
MAX_IMAGE_UPLOAD_SIZE = 10485760  # 10MB
