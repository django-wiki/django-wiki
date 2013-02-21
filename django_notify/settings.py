from django.conf import settings as django_settings

_ = lambda x: x

DB_TABLE_PREFIX = 'notify'

# You need to switch this setting on, otherwise nothing will happen :)
ENABLED = getattr(django_settings, "NOTIFY_ENABLED", True)

# Enable django-admin registration
ENABLE_ADMIN = getattr(django_settings, "NOTIFY_ENABLE_ADMIN", False)

##################################
# PLANNED CONFIGURATION SETTINGS #
##################################

# Email notifications are just optional... if you don't have access
# to a proper SMTP server, just leave it off...
SEND_EMAILS = getattr(django_settings, "NOTIFY_SEND_EMAILS", False)

EMAIL_SUBJECT = "Notifications" 

DEFAULT_EMAIL = 'notifications@example.com'
#NOTIFY_SLEEP_TIME must be greater than 0 to allow for Garbage Collection
NOTIFY_SLEEP_TIME = 10

# You can always make up more numbers... they simply identify which notifications
# to send when invoking the script, and the number indicates how many hours
# to minimum pass between each notification.
# Actual notifications are sent with a management script and a cron job!
INSTANTLY = 0
DAILY = 24-1 # Subtract 1, because the job finishes less than 24h before the next...
WEEKLY = 7*24-1

INTERVALS = getattr(django_settings, "NOTIFY_INTERVALS",
                    [(INSTANTLY, _(u'instant')),
                     (DAILY, _(u'daily')),
                     (WEEKLY, _(u'weekly'))])

INTERVALS_DEFAULT = INSTANTLY
# Minimum logging and digital garbage! Don't save too much crap!

# After how many days should viewed notifications be deleted?
AUTO_DELETE = getattr(django_settings, "NOTIFY_AUTO_DELETE", 120)

# After how many days should all types of notifications be deleted?
AUTO_DELETE_ALL = getattr(django_settings, "NOTIFY_AUTO_DELETE_ALL", 120)
