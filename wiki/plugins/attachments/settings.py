from django.conf import settings as django_settings

APP_LABEL = 'wiki'
SLUG = "attachments"

# Allow anonymous users to upload (not nice on an open network)
ANONYMOUS = getattr(django_settings, 'WIKI_ATTACHMENTS_ANONYMOUS', False)

# Maximum file sizes: Please using something like LimitRequestBody on
# your web server.
# http://httpd.apache.org/docs/2.2/mod/core.html#LimitRequestBody

# Where to store article attachments, relative to MEDIA_ROOT
# You should NEVER enable directory indexing in MEDIA_ROOT/UPLOAD_PATH !
# Actually, you can completely disable serving it, if you want. Files are
# sent to the user through a Django view that reads and streams a file.
UPLOAD_PATH = getattr(django_settings, 'WIKI_UPLOAD_PATH', 'wiki/uploads/%aid/')

# Should the upload path be obscurified? If so, a random hash will be added to the path
# such that someone can not guess the location of files (if you have
# restricted permissions and the files are still located within the web server's
UPLOAD_PATH_OBSCURIFY = getattr(django_settings, 'WIKI_UPLOAD_PATH_OBSCURIFY', True)

# Allowed extensions. Empty to disallow uploads completely.
# No files are saved without appending ".upload" to the file to ensure that
# your web server never actually executes some script.
# Case insensitive.
# You are asked to explicitly enter all file extensions that you want
# to allow. For your own safety.
FILE_EXTENSIONS = getattr(django_settings, 'WIKI_FILE_EXTENSIONS', ['pdf', 'doc', 'odt', 'docx', 'txt'])

from django.core.files.storage import default_storage
STORAGE_BACKEND = getattr(django_settings, 'WIKI_STORAGE_BACKEND', default_storage)