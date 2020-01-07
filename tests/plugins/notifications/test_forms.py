from django.test import TestCase
from tests.base import RequireSuperuserMixin
from wiki.plugins.notifications.forms import SettingsFormSet


class SettingsFormTests(RequireSuperuserMixin, TestCase):
    def test_formset(self):
        SettingsFormSet(user=self.superuser1)  # noqa
