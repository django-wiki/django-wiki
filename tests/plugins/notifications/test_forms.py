from django.test import TestCase
from django_nyt.forms import SettingsForm

from tests.base import RequireSuperuserMixin
from wiki.plugins.notifications.forms import SettingsFormSet


class SettingsFormTests(RequireSuperuserMixin, TestCase):
    def test_formset(self):
        formset = SettingsFormSet(user=self.superuser1)
