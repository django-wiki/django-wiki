from __future__ import unicode_literals

from django.conf import settings as django_settings
from wiki.conf import settings as wiki_settings

SLUG = 'images'

# Deprecated
APP_LABEL = None

#: Location where uploaded images are stored. ``%aid`` is replaced by the article id.
IMAGE_PATH = getattr(django_settings, 'WIKI_IMAGES_PATH', "wiki/images/%aid/")

#: Size for the image thumbnail included in the HTML text. If no specific
#: size is given in the markdown tag the ``default`` size is used. If a
#: specific size is given in the markdown tag that size is used.
THUMBNAIL_SIZES = getattr(django_settings, 'WIKI_IMAGES_THUMBNAIL_SIZES', {
    'default': '250x250',
    'small': '150x150',
    'medium': '300x300',
    'large': '500x500',
    'orig': None
})

#: Storage backend to use, default is to use the same as the rest of the
#: wiki, which is set in ``WIKI_STORAGE_BACKEND``, but you can override it
#: with ``WIKI_IMAGES_STORAGE_BACKEND``.
STORAGE_BACKEND = getattr(
    django_settings,
    'WIKI_IMAGES_STORAGE_BACKEND',
    wiki_settings.STORAGE_BACKEND)

#: Should the upload path be obscurified? If so, a random hash will be added
#: to the path such that someone can not guess the location of files (if you
#: have restricted permissions and the files are still located within the
#: web server's file system).
IMAGE_PATH_OBSCURIFY = getattr(
    django_settings,
    'WIKI_IMAGES_PATH_OBSCURIFY',
    True)

#: Allow anonymous users upload access (not nice on an open network).
#: ``WIKI_IMAGES_ANONYMOUS`` can override this, otherwise the default
#: in ``wiki.conf.settings`` is used.
ANONYMOUS = getattr(
    django_settings,
    'WIKI_IMAGES_ANONYMOUS',
    wiki_settings.ANONYMOUS_UPLOAD)
