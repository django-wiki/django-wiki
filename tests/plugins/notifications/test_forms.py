from django.test import TestCase
from wiki.plugins.notifications.forms import SettingsFormSet

from tests.base import RequireSuperuserMixin


class SettingsFormTests(RequireSuperuserMixin, TestCase):
    def test_formset(self):
        SettingsFormSet(user=self.superuser1)
