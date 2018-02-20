from django.test import TestCase
from wiki.conf import settings as wiki_settings
from wiki.forms import Group
from wiki.models import URLPath

from ..base import wiki_override_settings
from ..testdata.models import CustomGroup


class URLPathTests(TestCase):

    def test_manager(self):

        root = URLPath.create_root()
        child = URLPath.create_urlpath(root, "child")

        self.assertEqual(root.parent, None)
        self.assertEqual(list(root.children.all().active()), [child])


class CustomGroupTests(TestCase):
    @wiki_override_settings(WIKI_GROUP_MODEL='auth.Group')
    def test_setting(self):
        self.assertEqual(wiki_settings.GROUP_MODEL, 'auth.Group')

    def test_custom(self):
        self.assertEqual(Group, CustomGroup)
        self.assertEqual(wiki_settings.GROUP_MODEL, 'testdata.CustomGroup')
