from django.test import TestCase
from django_nyt.forms import SettingsForm
from wiki.plugins.notifications.forms import SettingsFormSet

from tests.base import RequireSuperuserMixin


class SettingsFormTests(RequireSuperuserMixin, TestCase):
    def test_formset(self):
        formset = SettingsFormSet(user=self.superuser1)
