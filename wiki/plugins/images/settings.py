from django.conf import settings as django_settings

# Where to store images
IMAGE_PATH = getattr(django_settings, 'WIKI_IMAGE_PATH', "wiki/images/%aid/")

# Should the upload path be obscurified? If so, a random hash will be added to the path
# such that someone can not guess the location of files (if you have
# restricted permissions and the files are still located within the web server's
IMAGE_PATH_OBSCURIFY = getattr(django_settings, 'WIKI_IMAGE_PATH_OBSCURIFY', True)

# Allow anonymous users to upload (not nice on an open network)
ANONYMOUS = getattr(django_settings, 'WIKI_ATTACHMENTS_ANONYMOUS', False)

SLUG = 'images'

APP_LABEL = 'wiki'