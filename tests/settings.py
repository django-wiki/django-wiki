import os

from django.urls import reverse_lazy

TESTS_DATA_ROOT = os.path.dirname(__file__)

MEDIA_ROOT = os.path.join(TESTS_DATA_ROOT, 'media')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

DEBUG = True
AUTH_USER_MODEL = 'testdata.CustomUser'
WIKI_GROUP_MODEL = 'testdata.CustomGroup'
SITE_ID = 1
ROOT_URLCONF = 'tests.testdata.urls'
INSTALLED_APPS = [
    'tests.testdata',
    'django.contrib.auth.apps.AuthConfig',
    'django.contrib.contenttypes.apps.ContentTypesConfig',
    'django.contrib.sessions.apps.SessionsConfig',
    'django.contrib.admin.apps.AdminConfig',
    'django.contrib.humanize.apps.HumanizeConfig',
    'django.contrib.sites.apps.SitesConfig',
    'django_nyt.apps.DjangoNytConfig',
    'mptt',
    'sekizai',
    'sorl.thumbnail',
    'wiki.apps.WikiConfig',
    'wiki.plugins.attachments.apps.AttachmentsConfig',
    'wiki.plugins.notifications.apps.NotificationsConfig',
    'wiki.plugins.images.apps.ImagesConfig',
    'wiki.plugins.macros.apps.MacrosConfig',
    'wiki.plugins.globalhistory.apps.GlobalHistoryConfig',
    "wiki.plugins.redlinks.apps.RedlinksConfig",
]
MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]
USE_TZ = True
SECRET_KEY = 'b^fv_)t39h%9p40)fnkfblo##jkr!$0)lkp6bpy!fi*f$4*92!'
STATIC_URL = '/static/'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "sekizai.context_processors.sekizai",
            ]
        },
    },
]

LOGIN_REDIRECT_URL = reverse_lazy('wiki:get', kwargs={'path': ''})
