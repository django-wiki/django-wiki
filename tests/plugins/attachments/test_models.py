from tests.base import RequireRootArticleMixin, TestBase
from wiki.plugins.attachments.models import Attachment, AttachmentRevision


class AttachmentRevisionTests(RequireRootArticleMixin, TestBase):

    def setUp(self):
        super().setUp()
        self.attachment = Attachment.objects.create(
            article=self.root_article, original_filename='blah.txt',
        )
        self.revision = AttachmentRevision.objects.create(
            attachment=self.attachment, file=None, description='muh',
            revision_number=1,
        )

    def test_revision_no_file(self):
        # Intentionally, there are no asserts, as the test just needs to
        # target an if-branch in the pre-delete signal for AttachmentRevision
        self.revision.delete()

    def test_revision_file_size(self):
        self.assertIsNone(self.revision.get_size())

    def test_get_filename_no_file(self):
        self.assertIsNone(self.revision.get_filename())

    def test_str(self):
        self.assertEqual(str(self.revision), "%s: %s (r%d)" % (
            'Root Article', 'blah.txt', 1,
        ))
