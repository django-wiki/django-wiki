from __future__ import absolute_import, unicode_literals

from testproject.settings import *
from testproject.settings.local import *

# Test codehilite with pygments

WIKI_MARKDOWN_KWARGS = {
    'extensions': [
        'codehilite',
        'footnotes',
        'attr_list',
        'headerid',
        'extra',
    ]}
