from __future__ import absolute_import
from __future__ import unicode_literals
from django import VERSION

# This is deprecated in django 1.7+
APP_LABEL = 'globalhistory' if VERSION < (1, 7) else None

SLUG = 'globalhistory'

RESULTS_PER_PAGE = 25
