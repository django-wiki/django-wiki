from __future__ import unicode_literals, absolute_import


try:
    from .local import *
except ImportError:
    from .base import *
