from __future__ import print_function, unicode_literals

from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse

from wiki.tests.base import ArticleWebTestBase


class AttachmentTests(ArticleWebTestBase):

    def setUp(self):
        super(AttachmentTests, self).setUp()
        self.article = self.root_article
        self.test_data = "This is a plain text file"
        self.test_description = 'My file'

    def _createTxtFilestream(self, strData, **kwargs):
        """
        Helper function to create filestream for upload.

        Parameters :
        strData : str, test string data

        Optional Arguments :
        filename : str, Defaults to 'test.txt'
        """
        filename = kwargs.get('filename', 'test.txt')
        data = strData.encode('utf-8')
        filedata = BytesIO(data)
        filestream = InMemoryUploadedFile(
            filedata,
            None,
            filename,
            'text',
            len(data),
            None
        )
        return filestream

    def _create_test_attachment(self):
        url = reverse('wiki:attachments_index', kwargs={'path': ''})
        filestream = self._createTxtFilestream(self.test_data)
        response = self.c.post(url,
                               {'description': self.test_description,
                                'file': filestream,
                                'save': '1',
                                })
        self.assertRedirects(response, url)

    def test_upload(self):
        """
        Tests that simple file upload uploads correctly
        Uploading a file should preserve the original filename.
        Uploading should not modify file in any way.
        """
        self._create_test_attachment()
        # Check the object was created.
        attachment = self.article.shared_plugins_set.all()[0].attachment
        self.assertEqual(attachment.original_filename, 'test.txt')
        self.assertEqual(attachment.current_revision.file.file.read(), self.test_data.encode('utf-8'))

    def test_replace(self):
        """
        Tests that previous revisions are not deleted
        Tests that only the most recent revision is deleted when
        "replace" is checked.
        """
        # Upload initial file
        url = reverse('wiki:attachments_index', kwargs={'path': ''})
        data = "This is a plain text file"
        filestream = self._createTxtFilestream(data)
        self.c.post(url, {'description': 'My file', 'file': filestream, 'save': '1', })
        attachment = self.article.shared_plugins_set.all()[0].attachment

        # uploading for the first time should mean that there is only one revision.
        self.assertEqual(attachment.attachmentrevision_set.count(), 1)

        # Change url to replacement page.
        url = reverse(
            'wiki:attachments_replace',
            kwargs={'attachment_id': attachment.id, 'article_id': self.article.id}
        )

        # Upload replacement without removing revisions
        replacement_data = data + ' And this is my edit'
        replacement_filestream = self._createTxtFilestream(replacement_data)
        self.c.post(
            url,
            {
                'description': 'Replacement upload',
                'file': replacement_filestream,
            }
        )
        attachment = self.article.shared_plugins_set.all()[0].attachment
        # Revision count should be two
        self.assertEqual(attachment.attachmentrevision_set.count(), 2)
        # Original filenames should not be modified
        self.assertEqual(attachment.original_filename, 'test.txt')
        # Latest revision should equal replacment_data
        self.assertEqual(attachment.current_revision.file.file.read(), replacement_data.encode('utf-8'))
        first_replacement = attachment.current_revision

        # Upload another replacement, this time removing most recent revision
        replacement_data2 = data + ' And this is a different edit'
        replacement_filestream2 = self._createTxtFilestream(replacement_data2)
        self.c.post(
            url,
            {
                'description': 'Replacement upload',
                'file': replacement_filestream2,
                'replace': 'on',
            }
        )
        attachment = self.article.shared_plugins_set.all()[0].attachment
        # Revision count should still be two
        self.assertEqual(attachment.attachmentrevision_set.count(), 2)
        # Latest revision should equal replacment_data2
        self.assertEqual(attachment.current_revision.file.file.read(), replacement_data2.encode('utf-8'))
        # The first replacement should no longer be in the filehistory
        self.assertNotIn(first_replacement, attachment.attachmentrevision_set.all())

    def test_search(self):
        """
        Call the search view
        """
        self._create_test_attachment()
        url = reverse('wiki:attachments_search', kwargs={'path': ''})
        response = self.c.get(url, {'query': self.test_description})
        self.assertContains(response, self.test_description)
