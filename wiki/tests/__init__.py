from __future__ import absolute_import

import django
if django.VERSION < (1, 6):
    # New style autodiscovery of tests doesn't work for Django < 1.6,
    # and we don't want to duplicate tests for Django >= 1.6
    from .test_basic import *
    from .test_managers import *
    from .test_models import *
    from .test_template_filters import *
    from .test_template_tags import *
    from .test_views import *
    from .test_urls import *
