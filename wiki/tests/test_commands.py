from __future__ import unicode_literals
from __future__ import absolute_import

import os
import sys
import tempfile

from .base import ArticleTestBase
from django.core.management import call_command


class TestManagementCommands(ArticleTestBase):
    """
    This clever test case can be inherited in other plugins

    Some data is created with ArticleTestBase, use that.
    """

    def test_dumpdata_loaddata(self):

        sysout = sys.stdout
        fixtures_file = tempfile.NamedTemporaryFile('w', delete=False, suffix=".json")
        sys.stdout = fixtures_file
        call_command('dumpdata', 'wiki')
        fixtures_file.file.flush()
        fixtures_file.file.close()
        sys.stdout = open(os.devnull, 'w')
        call_command('loaddata', fixtures_file.name)
        sys.stdout = sysout
        os.unlink(fixtures_file.name)
