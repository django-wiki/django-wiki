from django.test import TestCase
from django.utils.translation import gettext
from wiki.plugins.images.forms import PurgeForm


class PurgeFormTest(TestCase):
    def test_not_sure(self):
        form = PurgeForm(data={'confirm': False})
        self.assertIs(form.is_valid(), False)
        self.assertEqual(form.errors['confirm'], [gettext('You are not sure enough!')])

    def test_sure(self):
        form = PurgeForm(data={'confirm': True})
        self.assertIs(form.is_valid(), True)
