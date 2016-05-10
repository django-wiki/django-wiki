from __future__ import absolute_import

import django
if django.VERSION < (1, 6):
    # New style autodiscovery of tests doesn't work for Django < 1.6
    from .test_views import *  # noqa
