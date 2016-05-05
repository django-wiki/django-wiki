from __future__ import absolute_import, unicode_literals

import os
import tempfile

from wiki.tests.test_commands import TestManagementCommands

from .. import models


class TestAttachmentManagementCommands(TestManagementCommands):
    """
    Add some more data
    """

    def setUp(self):
        TestManagementCommands.setUp(self)

        self.test_file = tempfile.NamedTemporaryFile('w', delete=False, suffix=".txt")
        self.test_file.write("test")

        self.attachment1 = models.Attachment.objects.create(
            article=self.child1.article
        )

        self.attachment1_revision1 = models.AttachmentRevision.objects.create(
            attachment=self.attachment1,
            file=self.test_file.name,
        )

    def tearDown(self):
        os.unlink(self.test_file.name)
