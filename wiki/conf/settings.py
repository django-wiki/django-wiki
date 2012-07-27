# -*- coding: utf-8 -*-
from django.conf import settings as django_settings

# Should urls be case sensitive?
URL_CASE_SENSITIVE = getattr(django_settings, "WIKI_URL_CASE_SENSITIVE", False)

APP_LABEL = 'wiki'

# This slug is used in URLPath if an article has been deleted. The children of the
# URLPath of that article are moved to lost and found. They keep their permissions
# and all their content.
LOST_AND_FOUND_SLUG = getattr(django_settings, "WIKI_LOST_AND_FOUND_SLUG", 'lost-and-found')

# Where to store article attachments, relative to MEDIA_ROOT
UPLOAD_PATH = getattr(django_settings, "WIKI_UPLOAD_PATH", 'wiki/uploads/%aid/')

# Should the upload path be obscurified? If so, a random hash will be added to the path
# such that someone can not guess the location of files (if you have
# restricted permissions and the files are still located within the web server's
UPLOAD_PATH_OBSCURIFY = getattr(django_settings, "WIKI_UPLOAD_PATH_OBSCURIFY", True)

# Allowed non-image extensions. Empty to disallow completely.
# No files are saved without appending ".upload" to the file to ensure that
# your web server never actually executes some script.
# Case insensitive.
FILE_EXTENTIONS = getattr(django_settings, "WIKI_FILE_EXTENTIONS", ['pdf', 'doc', 'odt', 'docx', 'txt'])

# Where to store images
IMAGE_PATH = getattr(django_settings, "WIKI_IMAGE_PATH", 'wiki/images/%aid/')


####################
# PLANNED SETTINGS #
####################

# Maximum revisions to keep for an article, 0=unlimited
MAX_REVISIONS = getattr(django_settings, "WIKI_MAX_REVISIONS", 100)

# Maximum age of revisions in days, 0=unlimited
MAX_REVISION_AGE = getattr(django_settings, "MAX_REVISION_AGE", 365)

LOG_IPS_ANONYMOUS = getattr(django_settings, "WIKI_LOG_IPS_ANONYMOUS", True)
LOG_IPS_USERS = getattr(django_settings, "WIKI_LOG_IPS_USERS", False)

# Maximum allowed revisions per minute for any given user or IP
REVISIONS_PER_MINUTE = getattr(django_settings, "WIKI_REVISIONS_PER_MINUTE", 3)

# Allow others to upload
UPLOAD_OTHERS = getattr(django_settings, "WIKI_UPLOAD_OTHERS", True)

# Treat anonymous (non logged in) users as the "other" user group
ANONYMOUS = getattr(django_settings, "WIKI_ANONYMOUS", True)

# Globally enable write access for anonymous users, if true anonymous users will be treated
# as the others_write boolean field on models.Article. 
ANONYMOUS_WRITE = getattr(django_settings, "WIKI_ANONYMOUS_WRITE", False)
