from __future__ import absolute_import
from __future__ import unicode_literals
from django import VERSION
from django.conf import settings as django_settings
from wiki.conf import settings as wiki_settings
from django.core.exceptions import ImproperlyConfigured

# This is not used in django 1.7+
APP_LABEL = 'attachments' if VERSION < (1, 7) else None
SLUG = "attachments"

# Please see this note about support for UTF-8 files on django/apache:
# https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/modwsgi/#if-you-get-a-unicodeencodeerror

# Allow anonymous users upload access (not nice on an open network)
# WIKI_ATTACHMENTS_ANONYMOUS can override this, otherwise the default
# in wiki.conf.settings is used.
ANONYMOUS = getattr(
    django_settings,
    'WIKI_ATTACHMENTS_ANONYMOUS',
    wiki_settings.ANONYMOUS_UPLOAD)

# Maximum file sizes: Please using something like LimitRequestBody on
# your web server.
# http://httpd.apache.org/docs/2.2/mod/core.html#LimitRequestBody

# Where to store article attachments, relative to MEDIA_ROOT
# You should NEVER enable directory indexing in MEDIA_ROOT/UPLOAD_PATH !
# Actually, you can completely disable serving it, if you want. Files are
# sent to the user through a Django view that reads and streams a file.
UPLOAD_PATH = getattr(
    django_settings,
    'WIKI_ATTACHMENTS_PATH',
    'wiki/attachments/%aid/')

# Should the upload path be obscurified? If so, a random hash will be added to the path
# such that someone can not guess the location of files (if you have
# restricted permissions and the files are still located within the web
# server's
UPLOAD_PATH_OBSCURIFY = getattr(
    django_settings,
    'WIKI_ATTACHMENTS_PATH_OBSCURIFY',
    True)

# Allowed extensions. Empty to disallow uploads completely.
# No files are saved without appending ".upload" to the file to ensure that
# your web server never actually executes some script.
# Case insensitive.
# You are asked to explicitly enter all file extensions that you want
# to allow. For your own safety.
FILE_EXTENSIONS = getattr(
    django_settings, 'WIKI_ATTACHMENTS_EXTENSIONS',
    ['pdf', 'doc', 'odt', 'docx', 'txt'])

# Storage backend to use, default is to use the same as the rest of the
# wiki, which is set in WIKI_STORAGE_BACKEND, but you can override it
# with WIKI_ATTACHMENTS_STORAGE_BACKEND
STORAGE_BACKEND = getattr(
    django_settings,
    'WIKI_ATTACHMENTS_STORAGE_BACKEND',
    wiki_settings.STORAGE_BACKEND)

# SAFETY FIRST! Only store files with an appended .upload extension to be sure
# that something nasty does not get executed on the server.
APPEND_EXTENSION = getattr(
    django_settings,
    'WIKI_ATTACHMENTS_APPEND_EXTENSION',
    True)

# Important for S3 backends etc.: If your storage backend does not have a .path
# attribute for the file, but only a .url attribute, you should use False.
# This will reveal the direct download URL so it does not work perfectly for
# files you wish to be kept private.
USE_LOCAL_PATH = getattr(django_settings, 'WIKI_ATTACHMENTS_LOCAL_PATH', True)

if (not USE_LOCAL_PATH) and APPEND_EXTENSION:
    raise ImproperlyConfigured(
        "django-wiki (attachment plugin) not USE_LOCAL_PATH and APPEND_EXTENSION: "
        "You have configured to append .upload and not use local paths. That won't "
        "work as all your attachments will be stored and sent with a .upload "
        "extension. You have to trust your storage backend to be safe for storing"
        "the extensions you have allowed.")
