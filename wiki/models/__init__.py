from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import warnings

######################
# Configuration stuff
######################


######################
# Warnings
######################

if not 'south' in settings.INSTALLED_APPS:
    warnings.warn("You do not have south in your INSTALLED_APPS. This is highly discouraged.")