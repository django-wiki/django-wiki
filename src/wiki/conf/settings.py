import bleach
from django.conf import settings as django_settings
from django.contrib.messages import constants as messages
from django.core.files.storage import default_storage
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

#: Should urls be case sensitive?
URL_CASE_SENSITIVE = getattr(django_settings, 'WIKI_URL_CASE_SENSITIVE', False)

# Non-configurable (at the moment)
WIKI_LANGUAGE = 'markdown'

#: The editor class to use -- maybe a 3rd party or your own...? You can always
#: extend the built-in editor and customize it!
EDITOR = getattr(
    django_settings,
    'WIKI_EDITOR',
    'wiki.editors.markitup.MarkItUp')

#: Whether to use Bleach or not. It's not recommended to turn this off unless
#: you know what you're doing and you don't want to use the other options.
MARKDOWN_SANITIZE_HTML = getattr(
    django_settings,
    'WIKI_MARKDOWN_SANITIZE_HTML',
    True)

#: Arguments for the Markdown instance, as a dictionary. The "extensions" key
#: should be a list of extra extensions to use besides the built-in django-wiki
#: extensions, and the "extension_configs" should be a dictionary, specifying
#: the keyword-arguments to pass to each extension.
#:
#: For a list of extensions officially supported by Python-Markdown, see:
#: https://python-markdown.github.io/extensions/
#:
#: To set a custom title for table of contents, specify the following in your
#: Django project settings::
#:
#:     WIKI_MARKDOWN_KWARGS = {
#:         'extension_configs': {
#:             'wiki.plugins.macros.mdx.toc': {'title': 'Contents of this article'},
#:         },
#:     }
#:
#: Besides the extensions enabled by the "extensions" key, the following
#: built-in django-wiki extensions can be configured with "extension_configs":
#: "wiki.core.markdown.mdx.codehilite", "wiki.core.markdown.mdx.previewlinks",
#: "wiki.core.markdown.mdx.responsivetable", "wiki.plugins.macros.mdx.macro",
#: "wiki.plugins.macros.mdx.toc", "wiki.plugins.macros.mdx.wikilinks".
MARKDOWN_KWARGS = {
    'extensions': [
        'markdown.extensions.footnotes',
        'markdown.extensions.attr_list',
        'markdown.extensions.smart_strong',
        'markdown.extensions.footnotes',
        'markdown.extensions.attr_list',
        'markdown.extensions.def_list',
        'markdown.extensions.tables',
        'markdown.extensions.abbr',
        'markdown.extensions.sane_lists',
    ],
    'extension_configs': {
        'wiki.plugins.macros.mdx.toc': {'title': _('Contents')},
    },
}
MARKDOWN_KWARGS.update(getattr(django_settings, 'WIKI_MARKDOWN_KWARGS', {}))

_default_tag_whitelists = bleach.ALLOWED_TAGS + [
    'figure',
    'figcaption',
    'br',
    'hr',
    'p',
    'div',
    'img',
    'pre',
    'span',
    'sup',
    'table',
    'thead',
    'tbody',
    'th',
    'tr',
    'td',
    'dl',
    'dt',
    'dd',
] + ['h{}'.format(n) for n in range(8)]


#: List of allowed tags in Markdown article contents.
MARKDOWN_HTML_WHITELIST = _default_tag_whitelists
MARKDOWN_HTML_WHITELIST += (
    getattr(
        django_settings,
        'WIKI_MARKDOWN_HTML_WHITELIST',
        []
    )
)

_default_attribute_whitelist = bleach.ALLOWED_ATTRIBUTES
for tag in MARKDOWN_HTML_WHITELIST:
    if tag not in _default_attribute_whitelist:
        _default_attribute_whitelist[tag] = []
    _default_attribute_whitelist[tag].append('class')
    _default_attribute_whitelist[tag].append('id')

_default_attribute_whitelist['img'].append('src')
_default_attribute_whitelist['img'].append('alt')

#: Dictionary of allowed attributes in Markdown article contents.
MARKDOWN_HTML_ATTRIBUTES = _default_attribute_whitelist
MARKDOWN_HTML_ATTRIBUTES.update(
    getattr(
        django_settings,
        'WIKI_MARKDOWN_HTML_ATTRIBUTES',
        {}
    )
)

#: Allowed inline styles in Markdown article contents, default is no styles
#: (empty list).
MARKDOWN_HTML_STYLES = (
    getattr(
        django_settings,
        'WIKI_MARKDOWN_HTML_STYLES',
        []
    )
)

_project_defined_attrs = getattr(
    django_settings,
    'WIKI_MARKDOWN_HTML_ATTRIBUTE_WHITELIST',
    False)

# If styles are allowed but no custom attributes are defined, we allow styles
# for all kinds of tags.
if MARKDOWN_HTML_STYLES and not _project_defined_attrs:
    MARKDOWN_HTML_ATTRIBUTES['*'] = 'style'


#: This slug is used in URLPath if an article has been deleted. The children of the
#: URLPath of that article are moved to lost and found. They keep their permissions
#: and all their content.
LOST_AND_FOUND_SLUG = getattr(
    django_settings,
    'WIKI_LOST_AND_FOUND_SLUG',
    'lost-and-found')

#: When True, this blocks new slugs that resolve to non-wiki views, stopping
#: users creating articles that conflict with overlapping URLs from other apps.
CHECK_SLUG_URL_AVAILABLE = getattr(
    django_settings,
    'WIKI_CHECK_SLUG_URL_AVAILABLE',
    True)

#: Do we want to log IPs of anonymous users?
LOG_IPS_ANONYMOUS = getattr(django_settings, 'WIKI_LOG_IPS_ANONYMOUS', True)

#: Do we want to log IPs of logged in users?
LOG_IPS_USERS = getattr(django_settings, 'WIKI_LOG_IPS_USERS', False)

#: Mapping from message.tag to bootstrap class names.
MESSAGE_TAG_CSS_CLASS = getattr(
    django_settings,
    'WIKI_MESSAGE_TAG_CSS_CLASS',
    {
        messages.DEFAULT_TAGS[messages.DEBUG]: "alert alert-info",
        messages.DEFAULT_TAGS[messages.ERROR]: "alert alert-danger",
        messages.DEFAULT_TAGS[messages.INFO]: "alert alert-info",
        messages.DEFAULT_TAGS[messages.SUCCESS]: "alert alert-success",
        messages.DEFAULT_TAGS[messages.WARNING]: "alert alert-warning",
    }
)

####################################
# PERMISSIONS AND ACCOUNT HANDLING #
####################################

# NB! None of these callables need to handle anonymous users as they are treated
# in separate settings...

#: A function returning True/False if a user has permission to
#: read contents of an article and plugins.
#: Relevance: Viewing articles and plugins.
CAN_READ = getattr(django_settings, 'WIKI_CAN_READ', None)

#: A function returning True/False if a user has permission to
#: change contents, i.e. add new revisions to an article.
#: Often, plugins also use this.
#: Relevance: Editing articles, changing revisions, editing plugins.
CAN_WRITE = getattr(django_settings, 'WIKI_CAN_WRITE', None)

#: A function returning True/False if a user has permission to assign
#: permissions on an article.
#: Relevance: Changing owner and group membership.
CAN_ASSIGN = getattr(django_settings, 'WIKI_CAN_ASSIGN', None)

#: A function returning True/False if the owner of an article has permission
#: to change the group to a user's own groups.
#: Relevance: Changing group membership.
CAN_ASSIGN_OWNER = getattr(django_settings, 'WIKI_ASSIGN_OWNER', None)

#: A function returning True/False if a user has permission to change
#: read/write access for groups and others.
CAN_CHANGE_PERMISSIONS = getattr(
    django_settings,
    'WIKI_CAN_CHANGE_PERMISSIONS',
    None)

#: Specifies if a user has access to soft deletion of articles.
CAN_DELETE = getattr(django_settings, 'WIKI_CAN_DELETE', None)

#: A function returning True/False if a user has permission to change
#: moderate, ie. lock articles and permanently delete content.
CAN_MODERATE = getattr(django_settings, 'WIKI_CAN_MODERATE', None)

#: A function returning True/False if a user has permission to create
#: new groups and users for the wiki.
CAN_ADMIN = getattr(django_settings, 'WIKI_CAN_ADMIN', None)

#: Treat anonymous (i.e. non logged in) users as the "other" user group.
ANONYMOUS = getattr(django_settings, 'WIKI_ANONYMOUS', True)

#: Globally enable write access for anonymous users, if true anonymous users
#: will be treated as the others_write boolean field on models.Article.
ANONYMOUS_WRITE = getattr(django_settings, 'WIKI_ANONYMOUS_WRITE', False)

#: Globally enable create access for anonymous users.
#: Defaults to ``ANONYMOUS_WRITE``.
ANONYMOUS_CREATE = getattr(
    django_settings,
    'WIKI_ANONYMOUS_CREATE',
    ANONYMOUS_WRITE)

#: Default setting to allow anonymous users upload access. Used in
#: plugins.attachments and plugins.images, and can be overwritten in
#: these plugins.
ANONYMOUS_UPLOAD = getattr(django_settings, 'WIKI_ANONYMOUS_UPLOAD', False)

#: Sign up, login and logout views should be accessible.
ACCOUNT_HANDLING = getattr(django_settings, 'WIKI_ACCOUNT_HANDLING', True)

#: Signup allowed? If it's not allowed, logged in superusers can still access
#: the signup page to create new users.
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

#: Maximum amount of children to display in a menu before showing "+more".
#: NEVER set this to 0 as it will wrongly inform the user that there are no
#: children and for instance that an article can be safely deleted.
SHOW_MAX_CHILDREN = getattr(django_settings, 'WIKI_SHOW_MAX_CHILDREN', 20)

#: User Bootstrap's select widget. Switch off if you're not using Bootstrap!
USE_BOOTSTRAP_SELECT_WIDGET = getattr(
    django_settings,
    'WIKI_USE_BOOTSTRAP_SELECT_WIDGET',
    True)

#: Dotted name of the class used to construct urlpatterns for the wiki.
#: Default is wiki.urls.WikiURLPatterns. To customize urls or view handlers,
#: you can derive from this.
URL_CONFIG_CLASS = getattr(
    django_settings,
    'WIKI_URL_CONFIG_CLASS',
    None)

#: Seconds of timeout before renewing the article cache. Articles are automatically
#: renewed whenever an edit occurs but article content may be generated from
#: other objects that are changed.
CACHE_TIMEOUT = getattr(django_settings, 'WIKI_CACHE_TIMEOUT', 600)

#: Choose the Group model to use for permission handling. Defaults to django's auth.Group.
GROUP_MODEL = getattr(django_settings, 'WIKI_GROUP_MODEL', 'auth.Group')

###################
# SPAM PROTECTION #
###################

#: Maximum allowed revisions per hour for any given user or IP.
REVISIONS_PER_HOUR = getattr(django_settings, 'WIKI_REVISIONS_PER_HOUR', 60)

#: Maximum allowed revisions per minute for any given user or IP.
REVISIONS_PER_MINUTES = getattr(
    django_settings,
    'WIKI_REVISIONS_PER_MINUTES',
    5)

#: Maximum allowed revisions per hour for any anonymous user and any IP.
REVISIONS_PER_HOUR_ANONYMOUS = getattr(
    django_settings,
    'WIKI_REVISIONS_PER_HOUR_ANONYMOUS',
    10)

#: Maximum allowed revisions per minute for any anonymous user and any IP.
REVISIONS_PER_MINUTES_ANONYMOUS = getattr(
    django_settings,
    'WIKI_REVISIONS_PER_MINUTES_ANONYMOUS',
    2)

#: Number of minutes to look back for looking up ``REVISIONS_PER_MINUTES``
#: and ``REVISIONS_PER_MINUTES_ANONYMOUS``.
REVISIONS_MINUTES_LOOKBACK = getattr(
    django_settings,
    'WIKI_REVISIONS_MINUTES_LOOKBACK',
    2)

###########
# STORAGE #
###########

#: Default Django storage backend to use for images, attachments etc.
STORAGE_BACKEND = getattr(
    django_settings,
    'WIKI_STORAGE_BACKEND',
    default_storage)

#: Use django-sendfile for sending out files? Otherwise the whole file is
#: first read into memory and than send with a mime type based on the file.
USE_SENDFILE = getattr(django_settings, 'WIKI_ATTACHMENTS_USE_SENDFILE', False)
