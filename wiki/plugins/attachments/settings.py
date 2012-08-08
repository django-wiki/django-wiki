from django.conf import settings as django_settings

SLUG = "attachments"

# Where to store article attachments, relative to MEDIA_ROOT
UPLOAD_PATH = getattr(django_settings, 'WIKI_UPLOAD_PATH', 'wiki/uploads/%aid/')

# Should the upload path be obscurified? If so, a random hash will be added to the path
# such that someone can not guess the location of files (if you have
# restricted permissions and the files are still located within the web server's
UPLOAD_PATH_OBSCURIFY = getattr(django_settings, 'WIKI_UPLOAD_PATH_OBSCURIFY', True)

# Allowed non-image extensions. Empty to disallow completely.
# No files are saved without appending ".upload" to the file to ensure that
# your web server never actually executes some script.
# Case insensitive.
FILE_EXTENSIONS = getattr(django_settings, 'WIKI_FILE_EXTENSIONS', ['pdf', 'doc', 'odt', 'docx', 'txt'])
