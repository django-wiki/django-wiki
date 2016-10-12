from __future__ import absolute_import, unicode_literals

from django.conf import settings as django_settings
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

# Should urls be case sensitive?
URL_CASE_SENSITIVE = getattr(django_settings, 'WIKI_URL_CASE_SENSITIVE', False)

# Non-configurable (at the moment)
WIKI_LANGUAGE = 'markdown'

# The editor class to use -- maybe a 3rd party or your own...? You can always
# extend the built-in editor and customize it....
EDITOR = getattr(
    django_settings,
    'WIKI_EDITOR',
    'wiki.editors.markitup.MarkItUp')

MARKDOWN_KWARGS = {
    'extensions': [
        'footnotes',
        'attr_list',
        'extra',
        'codehilite',
        'sane_lists',
    ],
    'safe_mode': 'replace',
    'extension_configs': {
        'toc': {
            'title': _('Table of Contents')}},
}
MARKDOWN_KWARGS.update(getattr(django_settings, 'WIKI_MARKDOWN_KWARGS', {}))

# This slug is used in URLPath if an article has been deleted. The children of the
# URLPath of that article are moved to lost and found. They keep their permissions
# and all their content.
LOST_AND_FOUND_SLUG = getattr(
    django_settings,
    'WIKI_LOST_AND_FOUND_SLUG',
    'lost-and-found')

# When True, this blocks new slugs that resolve to non-wiki views, stopping
# users creating articles that conflict with overlapping URLs from other apps.
CHECK_SLUG_URL_AVAILABLE = getattr(
    django_settings,
    'WIKI_CHECK_SLUG_URL_AVAILABLE',
    True)

# Do we want to log IPs?
LOG_IPS_ANONYMOUS = getattr(django_settings, 'WIKI_LOG_IPS_ANONYMOUS', True)
LOG_IPS_USERS = getattr(django_settings, 'WIKI_LOG_IPS_USERS', False)

####################################
# PERMISSIONS AND ACCOUNT HANDLING #
####################################

# NB! None of these callables need to handle anonymous users as they are treated
# in separate settings...

# A function returning True/False if a user has permission to
# read contents of an article + plugins
# Relevance: viewing articles and plugins
CAN_READ = getattr(django_settings, 'WIKI_CAN_READ', None)

# A function returning True/False if a user has permission to
# change contents, ie add new revisions to an article
# Often, plugins also use this
# Relevance: editing articles, changing revisions, editing plugins
CAN_WRITE = getattr(django_settings, 'WIKI_CAN_WRITE', None)

# A function returning True/False if a user has permission to assign
# permissions on an article
# Relevance: changing owner and group membership
CAN_ASSIGN = getattr(django_settings, 'WIKI_CAN_ASSIGN', None)

# A function returning True/False if the owner of an article has permission to change
# the group to a user's own groups
# Relevance: changing group membership
CAN_ASSIGN_OWNER = getattr(django_settings, 'WIKI_ASSIGN_OWNER', None)

# A function returning True/False if a user has permission to change
# read/write access for groups and others
CAN_CHANGE_PERMISSIONS = getattr(
    django_settings,
    'WIKI_CAN_CHANGE_PERMISSIONS',
    None)

# Specifies if a user has access to soft deletion of articles
CAN_DELETE = getattr(django_settings, 'WIKI_CAN_DELETE', None)

# A function returning True/False if a user has permission to change
# moderate, ie. lock articles and permanently delete content.
CAN_MODERATE = getattr(django_settings, 'WIKI_CAN_MODERATE', None)

# A function returning True/False if a user has permission to create
# new groups and users for the wiki.
CAN_ADMIN = getattr(django_settings, 'WIKI_CAN_ADMIN', None)

# Treat anonymous (non logged in) users as the "other" user group
ANONYMOUS = getattr(django_settings, 'WIKI_ANONYMOUS', True)

# Globally enable write access for anonymous users, if true anonymous users will be treated
# as the others_write boolean field on models.Article.
ANONYMOUS_WRITE = getattr(django_settings, 'WIKI_ANONYMOUS_WRITE', False)

# Globally enable create access for anonymous users
# Defaults to ANONYMOUS_WRITE.
ANONYMOUS_CREATE = getattr(
    django_settings,
    'WIKI_ANONYMOUS_CREATE',
    ANONYMOUS_WRITE)

# Default setting to allow anonymous users upload access (used in
# plugins.attachments and plugins.images).
ANONYMOUS_UPLOAD = getattr(django_settings, 'WIKI_ANONYMOUS_UPLOAD', False)

# Sign up, login and logout views should be accessible
ACCOUNT_HANDLING = getattr(django_settings, 'WIKI_ACCOUNT_HANDLING', True)

# Signup allowed? If it's not allowed, logged in superusers can still access
# the signup page to create new users.
ACCOUNT_SIGNUP_ALLOWED = ACCOUNT_HANDLING and getattr(
    django_settings, 'WIKI_ACCOUNT_SIGNUP_ALLOWED', True
)

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

USE_BOOTSTRAP_SELECT_WIDGET = getattr(
    django_settings,
    'WIKI_USE_BOOTSTRAP_SELECT_WIDGET',
    True)

#: dottedname of class used to construct urlpatterns for wiki.
#:
#: Default is wiki.urls.WikiURLPatterns. To customize urls or view handlers,
#: you can derive from this.
URL_CONFIG_CLASS = getattr(
    django_settings,
    'WIKI_URL_CONFIG_CLASS',
    'wiki.urls.WikiURLPatterns')

# Search view - dotted path denoting where the search view Class is located
SEARCH_VIEW = getattr(
    django_settings,
    'WIKI_SEARCH_VIEW',
    'wiki.views.article.SearchView'
    if 'wiki.plugins.haystack' not in django_settings.INSTALLED_APPS
    else
    'wiki.plugins.haystack.views.HaystackSearchView'
)

# Seconds of timeout before renewing article cache. Articles are automatically
# renewed whenever an edit occurs but article content may be generated from
# other objects that are changed.
CACHE_TIMEOUT = getattr(django_settings, 'WIKI_CACHE_TIMEOUT', 600)

# Choose the Group model to use. Defaults to django's auth.Group
GROUP_MODEL = getattr(django_settings, 'WIKI_GROUP_MODEL', 'auth.Group')

###################
# SPAM PROTECTION #
###################

# Maximum allowed revisions per hour for any given user or IP
REVISIONS_PER_HOUR = getattr(django_settings, 'WIKI_REVISIONS_PER_HOUR', 60)

# Maximum allowed revisions per minute for any given user or IP
REVISIONS_PER_MINUTES = getattr(
    django_settings,
    'WIKI_REVISIONS_PER_MINUTES',
    5)

# Maximum allowed revisions per hour for any given user or IP
REVISIONS_PER_HOUR_ANONYMOUS = getattr(
    django_settings,
    'WIKI_REVISIONS_PER_HOUR_ANONYMOUS',
    10)

# Maximum allowed revisions per hour for any given user or IP
REVISIONS_PER_MINUTES_ANONYMOUS = getattr(
    django_settings,
    'WIKI_REVISIONS_PER_MINUTES_ANONYMOUS',
    2)

# Number of minutes for looking up REVISIONS_PER_MINUTES and
# REVISIONS_PER_MINUTES_ANONYMOUS
REVISIONS_MINUTES_LOOKBACK = getattr(
    django_settings,
    'WIKI_REVISIONS_MINUTES_LOOKBACK',
    2)

###########
# STORAGE #
###########

STORAGE_BACKEND = getattr(
    django_settings,
    'WIKI_STORAGE_BACKEND',
    default_storage)

USE_SENDFILE = getattr(django_settings, 'WIKI_ATTACHMENTS_USE_SENDFILE', False)

####################
# PLANNED SETTINGS #
####################

# Maximum revisions to keep for an article, 0=unlimited
MAX_REVISIONS = getattr(django_settings, 'WIKI_MAX_REVISIONS', 100)

# Maximum age of revisions in days, 0=unlimited
MAX_REVISION_AGE = getattr(
    django_settings, 'WIKI_MAX_REVISION_AGE',
    getattr(django_settings, 'MAX_REVISION_AGE', 365)
)
