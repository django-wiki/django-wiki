from __future__ import print_function, unicode_literals

from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse

from wiki.tests.base import ArticleTestBase


class AttachmentTests(ArticleTestBase):

    def test_upload(self):
        data = "This is a plain text file".encode('utf-8')
        filedata = BytesIO(data)
        filestream = InMemoryUploadedFile(
            filedata,
            None,
            'test.txt',
            'text',
            len(data),
            None)
        article = self.root_article
        url = reverse('wiki:attachments_index', kwargs={'path': ''})
        response = self.c.post(url,
                               {'description': 'My file',
                                'file': filestream,
                                'save': '1',
                                })
        self.assertRedirects(response, url)
        # Check the object was created.
        attachment = article.shared_plugins_set.all()[0].attachment
        self.assertEqual(attachment.original_filename, 'test.txt')
        self.assertEqual(attachment.current_revision.file.file.read(),
                         data)
