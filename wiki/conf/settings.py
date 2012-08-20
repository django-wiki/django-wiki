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

# If you want to write an extension, you should use the plugin API as you
# will get an article model instance to play with. These are just the
# builtin markdown extensions
# Notice that this should be a callable which accepts the article as an argument
def get_extensions(article):
    from wiki.models import URLPath
    try:
        urlpath = URLPath.objects.get(article=article)
        url = reverse_lazy('wiki:get', kwargs={'path': urlpath.path})
    except URLPath.DoesNotExist:
        url = reverse_lazy('wiki:get', kwargs={'article_id': article.id})
    return ['extra', 'wikilinks(base_url=%s)' % url, 'codehilite(force_linenos=True)', 'toc']
MARKDOWN_EXTENSIONS = getattr(
    django_settings, 
    'WIKI_MARKDOWN_EXTENSIONS',
    get_extensions 
)

# This slug is used in URLPath if an article has been deleted. The children of the
# URLPath of that article are moved to lost and found. They keep their permissions
# and all their content.
LOST_AND_FOUND_SLUG = getattr(django_settings, 'WIKI_LOST_AND_FOUND_SLUG', 'lost-and-found')

# Do we want to log IPs?
LOG_IPS_ANONYMOUS = getattr(django_settings, 'WIKI_LOG_IPS_ANONYMOUS', True)
LOG_IPS_USERS = getattr(django_settings, 'WIKI_LOG_IPS_USERS', False)

# Sign up, login and logout views should be accessible 
ACCOUNT_HANDLING = getattr(django_settings, 'WIKI_ACCOUNT_HANDLING', True)

if ACCOUNT_HANDLING:
    LOGIN_URL = reverse_lazy("wiki:login")
else:
    LOGIN_URL = getattr(django_settings, "LOGIN_URL", "/")

# Maximum amount of children to display in a menu before going "+more"
SHOW_MAX_CHILDREN = getattr(django_settings, 'WIKI_SHOW_MAX_CHILDREN', 20)

####################
# PLANNED SETTINGS #
####################

# Maximum revisions to keep for an article, 0=unlimited
MAX_REVISIONS = getattr(django_settings, 'WIKI_MAX_REVISIONS', 100)

# Maximum age of revisions in days, 0=unlimited
MAX_REVISION_AGE = getattr(django_settings, 'MAX_REVISION_AGE', 365)

# Maximum allowed revisions per minute for any given user or IP
REVISIONS_PER_MINUTE = getattr(django_settings, 'WIKI_REVISIONS_PER_MINUTE', 3)

# Allow others to upload
UPLOAD_OTHERS = getattr(django_settings, 'WIKI_UPLOAD_OTHERS', True)

# Treat anonymous (non logged in) users as the "other" user group
ANONYMOUS = getattr(django_settings, 'WIKI_ANONYMOUS', True)

# Globally enable write access for anonymous users, if true anonymous users will be treated
# as the others_write boolean field on models.Article. 
ANONYMOUS_WRITE = getattr(django_settings, 'WIKI_ANONYMOUS_WRITE', False)
