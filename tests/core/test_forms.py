from django.test import TestCase
from django.utils.translation import gettext
from tests.base import DjangoClientTestBase, RequireRootArticleMixin
from wiki.forms import DeleteForm, UserCreationForm


class DeleteFormTests(RequireRootArticleMixin, DjangoClientTestBase):
    def test_not_sure(self):
        data = {'purge': True, 'confirm': False}
        form = DeleteForm(article=self.root_article, has_children=True, data=data)
        self.assertIs(form.is_valid(), False)
        self.assertEqual(form.errors['__all__'], [gettext('You are not sure enough!')])


class UserCreationFormTests(TestCase):
    def test_honeypot(self):
        data = {
            'address': 'Wiki Road 123', 'phone': '12345678', 'email': 'wiki@wiki.com',
            'username': 'WikiMan', 'password1': 'R@ndomString', 'password2': 'R@ndomString'
        }
        form = UserCreationForm(data=data)
        self.assertIs(form.is_valid(), False)
        self.assertEqual(
            form.errors['__all__'],
            ["Thank you, non-human visitor. Please keep trying to fill in the form."]
        )
