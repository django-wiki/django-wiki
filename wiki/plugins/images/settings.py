from django.conf import settings as django_settings

# Where to store images
IMAGE_PATH = getattr(django_settings, 'WIKI_IMAGE_PATH', "wiki/images/%aid/")

# Allow anonymous users to upload (not nice on an open network)
ANONYMOUS = getattr(django_settings, 'WIKI_ATTACHMENTS_ANONYMOUS', False)

SLUG = 'images'

APP_LABEL = 'wiki'