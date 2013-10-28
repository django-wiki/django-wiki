from django.conf import settings as django_settings
from django import VERSION as DJANGO_VERSION
from django.utils.translation import ugettext_lazy as _


DB_TABLE_PREFIX = 'notify'

# You need to switch this setting on, otherwise nothing will happen :)
ENABLED = getattr(django_settings, 'NOTIFY_ENABLED', True)

# Enable django-admin registration
ENABLE_ADMIN = getattr(django_settings, 'NOTIFY_ENABLE_ADMIN', False)

# Email notifications won't get sent unless you run
# python manage.py notifymail
SEND_EMAILS = getattr(django_settings, 'NOTIFY_SEND_EMAILS', True)

EMAIL_SUBJECT = getattr(django_settings, 
    'NOTIFY_EMAIL_SUBJECT', _("You have new notifications")) 

EMAIL_SENDER = getattr(django_settings, 
    'NOTIFY_EMAIL_SENDER', "notifications@example.com")

# Seconds to sleep between each database poll
# (leave high unless you really want to send extremely real time
# notifications)
NOTIFY_SLEEP_TIME = 120

# You can always make up more numbers... they simply identify which notifications
# to send when invoking the script, and the number indicates how many hours
# to minimum pass between each notification.
INSTANTLY = 0
DAILY = (24 - 1) * 60 # Subtract 1, because the job finishes less than 24h before the next...
WEEKLY = 7 * (24 - 1) * 60

# List of intervals available. In minutes
INTERVALS = getattr(django_settings, 'NOTIFY_INTERVALS',
    [(INSTANTLY, _(u'instantly')),
     (DAILY, _(u'daily')),
     (WEEKLY, _(u'weekly'))]
)

INTERVALS_DEFAULT = INSTANTLY

# Django 1.5+
if DJANGO_VERSION >= (1,5):
    USER_MODEL = getattr(django_settings, 'AUTH_USER_MODEL', 'auth.User')
else:
    USER_MODEL = 'auth.User'

####################
# PLANNED SETTINGS #
####################

# Minimum logging and digital garbage! Don't save too much crap!

# After how many days should viewed notifications be deleted?
AUTO_DELETE = getattr(django_settings, 'NOTIFY_AUTO_DELETE', 120)

# After how many days should all types of notifications be deleted?
AUTO_DELETE_ALL = getattr(django_settings, 'NOTIFY_AUTO_DELETE_ALL', 120)

NOTIFY_LOG = getattr(django_settings, 'NOTIFY_LOG', '/tmp/daemon_notify.log')

NOTIFY_PID = getattr(django_settings, 'NOTIFY_PID', '/tmp/daemon_notify.pid')


