import os
import tempfile

from tests.core.test_commands import TestManagementCommands
from wiki.models import URLPath
from wiki.plugins.attachments import models


class TestAttachmentManagementCommands(TestManagementCommands):
    """
    Add some more data
    """

    def setUp(self):
        super().setUp()

        self.test_file = tempfile.NamedTemporaryFile('w', delete=False, suffix=".txt")
        self.test_file.write("test")

        self.child1 = URLPath.create_urlpath(self.root, 'test-slug', title="Test 1")

        self.attachment1 = models.Attachment.objects.create(
            article=self.child1.article
        )

        self.attachment1_revision1 = models.AttachmentRevision.objects.create(
            attachment=self.attachment1,
            file=self.test_file.name,
        )

    def tearDown(self):
        os.unlink(self.test_file.name)
        super().tearDown()
