from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

class WebClientTest(TestCase):
    def test_preview_save(self):
        """Test the basic operations (create, preview and save the article) by web client."""
        c = Client()
        User.objects.create_superuser('admin', 'nobody@example.com', 'secret')
        c.login(username='admin', password='secret')
        response = c.get(reverse('wiki:root'))  # url '/'
        self.assertRedirects(response, reverse('wiki:root_create'))  # url '/create-root/'

        # test create the root article
        response = c.post(reverse('wiki:root_create'),
                {'content': 'test heading h1\n====\n', 'save_changes': 'Create root...', 'title': 'wiki test'})
        self.assertRedirects(response, reverse('wiki:root'))
        response = c.get(reverse('wiki:root'))
        self.assertContains(response, 'test heading h1</h1>')

        # test preview
        form_data = {
                'content': 'The modified text',
                'current_revision': '1',
                'preview': '1',
                'save': '1',
                'summary': 'any summary',
                'title': 'wiki test'}
        response = c.post(reverse('wiki:preview', kwargs={'path': ''}), form_data)  # url: '/_preview/'
        self.assertContains(response, 'The modified text')  # preview failed

        # test save
        response = c.post(reverse('wiki:edit', kwargs={'path': ''}), form_data)
        message = c.cookies['messages'].value if 'messages' in c.cookies else None
        self.assertRedirects(response, reverse('wiki:root'))
        response = c.get(reverse('wiki:root'))
        self.assertContains(response, 'The modified text')
        # test messages
        self.assertTrue('succesfully added' in message)
