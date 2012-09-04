# -*- coding: utf-8 -*-
from django.conf import settings as django_settings
from django.core.urlresolvers import reverse_lazy

# Should urls be case sensitive?
URL_CASE_SENSITIVE = getattr(django_settings, 'WIKI_URL_CASE_SENSITIVE', False)

# Non-configurable (at the moment)
APP_LABEL = 'wiki'
WIKI_LANGUAGE = 'markdown'

# The editor class to use -- maybe a 3rd party or your own...? You can always
# extend the built-in editor and customize it....
EDITOR = getattr(django_settings, 'WIKI_EDITOR', 'wiki.editors.markitup.MarkItUp')

MARKDOWN_EXTENSIONS = getattr(django_settings, 'WIKI_MARKDOWN_EXTENSIONS', ['extra', 'toc'])

# This slug is used in URLPath if an article has been deleted. The children of the
# URLPath of that article are moved to lost and found. They keep their permissions
# and all their content.
LOST_AND_FOUND_SLUG = getattr(django_settings, 'WIKI_LOST_AND_FOUND_SLUG', 'lost-and-found')

# Do we want to log IPs?
LOG_IPS_ANONYMOUS = getattr(django_settings, 'WIKI_LOG_IPS_ANONYMOUS', True)
LOG_IPS_USERS = getattr(django_settings, 'WIKI_LOG_IPS_USERS', False)

####################################
# PERMISSIONS AND ACCOUNT HANDLING #
####################################

# NB! None of these callables need to handle anonymous users as they are treated
# in separate settings...

# A function returning True/False if a user has permission to assign
# permissions on an article
# Relevance: changing owner and group membership
CAN_ASSIGN = getattr(django_settings, 'WIKI_CAN_ASSIGN', lambda article, user: user.has_perm('wiki.assign'))

# A function returning True/False if the owner of an article has permission to change
# the group to a user's own groups
# Relevance: changing group membership
CAN_ASSIGN_OWNER = getattr(django_settings, 'WIKI_ASSIGN_OWNER', lambda article, user: False)

# A function returning True/False if a user has permission to change
# read/write access for groups and others
CAN_CHANGE_PERMISSIONS = getattr(django_settings, 'WIKI_CAN_CHANGE_PERMISSIONS', lambda article, user: article.owner == user or user.has_perm('wiki.assign'))

# Specifies if a user has access to soft deletion of articles
CAN_DELETE = getattr(django_settings, 'WIKI_CAN_DELETE', lambda article, user: article.can_write(user=user))

# A function returning True/False if a user has permission to change
# moderate, ie. lock articles and permanently delete content.
CAN_MODERATE = getattr(django_settings, 'WIKI_CAN_MODERATE', lambda article, user: user.has_perm('wiki.moderate'))

# A function returning True/False if a user has permission to create
# new groups and users for the wiki.
CAN_ADMIN = getattr(django_settings, 'WIKI_CAN_ADMIN', lambda article, user: user.has_perm('wiki.admin'))

# Treat anonymous (non logged in) users as the "other" user group
ANONYMOUS = getattr(django_settings, 'WIKI_ANONYMOUS', True)

# Globally enable write access for anonymous users, if true anonymous users will be treated
# as the others_write boolean field on models.Article. 
ANONYMOUS_WRITE = getattr(django_settings, 'WIKI_ANONYMOUS_WRITE', False)

# Sign up, login and logout views should be accessible 
ACCOUNT_HANDLING = getattr(django_settings, 'WIKI_ACCOUNT_HANDLING', True)

if ACCOUNT_HANDLING:
    LOGIN_URL = reverse_lazy("wiki:login")
    LOGOUT_URL = reverse_lazy("wiki:logout")
    SIGNUP_URL = reverse_lazy("wiki:signup")
else:
    LOGIN_URL = getattr(django_settings, "LOGIN_URL", "/")
    LOGOUT_URL = getattr(django_settings, "LOGOUT_URL", "/")
    SIGNUP_URL = getattr(django_settings, "WIKI_SIGNUP_URL", "/")

##################
# OTHER SETTINGS #
##################

# Maximum amount of children to display in a menu before going "+more"
# NEVER set this to 0 as it will wrongly inform the user that there are no
# children and for instance that an article can be safely deleted.
SHOW_MAX_CHILDREN = getattr(django_settings, 'WIKI_SHOW_MAX_CHILDREN', 20)

USE_BOOTSTRAP_SELECT_WIDGET = getattr(django_settings, 'WIKI_USE_BOOTSTRAP_SELECT_WIDGET', True)

####################
# PLANNED SETTINGS #
####################

# Maximum revisions to keep for an article, 0=unlimited
MAX_REVISIONS = getattr(django_settings, 'WIKI_MAX_REVISIONS', 100)

# Maximum age of revisions in days, 0=unlimited
MAX_REVISION_AGE = getattr(django_settings, 'MAX_REVISION_AGE', 365)

# Maximum allowed revisions per minute for any given user or IP
REVISIONS_PER_MINUTE = getattr(django_settings, 'WIKI_REVISIONS_PER_MINUTE', 3)
