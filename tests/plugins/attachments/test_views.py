from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from wiki.models import URLPath

from ...base import ArticleWebTestUtils, DjangoClientTestBase, RequireRootArticleMixin


class AttachmentTests(RequireRootArticleMixin, ArticleWebTestUtils, DjangoClientTestBase):

    def setUp(self):
        super().setUp()
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

    def _create_test_attachment(self, path):
        url = reverse('wiki:attachments_index', kwargs={'path': path})
        filestream = self._createTxtFilestream(self.test_data)
        response = self.client.post(
            url,
            {
                'description': self.test_description,
                'file': filestream,
                'save': '1',
            }
        )
        self.assertRedirects(response, url)

    def test_upload(self):
        """
        Tests that simple file upload uploads correctly
        Uploading a file should preserve the original filename.
        Uploading should not modify file in any way.
        """
        self._create_test_attachment('')
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
        self.client.post(url, {'description': 'My file', 'file': filestream, 'save': '1', })
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
        self.client.post(
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
        self.client.post(
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
        self._create_test_attachment('')
        url = reverse('wiki:attachments_search', kwargs={'path': ''})
        response = self.client.get(url, {'query': self.test_description})
        self.assertContains(response, self.test_description)

    def get_article(self, cont):
        urlpath = URLPath.create_urlpath(
            URLPath.root(),
            "html_attach",
            title="TestAttach",
            content=cont
        )
        self._create_test_attachment(urlpath.path)
        return urlpath.article.render()

    def test_render(self):
        output = self.get_article('[attachment:1]')
        expected = (
            '<span class="attachment"><a href=".*attachments/download/1/"'
            ' title="Click to download test\.txt">\s*test\.txt\s*</a>'
        )
        self.assertRegexpMatches(output, expected)

    def test_render_missing(self):
        output = self.get_article('[attachment:2]')
        expected = (
            '<span class="attachment attachment-deleted">\s*Attachment with ID #2 is deleted.\s*</span>'
        )
        self.assertRegexpMatches(output, expected)

    def test_render_title(self):
        output = self.get_article('[attachment:1 title:"Test title"]')
        expected = (
            '<span class="attachment"><a href=".*attachments/download/1/"'
            ' title="Click to download test\.txt">\s*Test title\s*</a>'
        )
        self.assertRegexpMatches(output, expected)

    def test_render_title_size(self):
        output = self.get_article('[attachment:1 title:"Test title 2" size]')
        expected = (
            '<span class="attachment"><a href=".*attachments/download/1/"'
            ' title="Click to download test\.txt">\s*Test title 2 \[25[^b]bytes\]\s*</a>'
        )
        self.assertRegexpMatches(output, expected)
