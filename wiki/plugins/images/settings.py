from django.conf import settings as django_settings

# Where to store images
IMAGE_PATH = getattr(django_settings, 'WIKI_IMAGE_PATH', "wiki/images/%aid/")

SLUG = 'images'