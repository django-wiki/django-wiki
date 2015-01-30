from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from django.test import TestCase

from wiki.models import URLPath


class URLPathTests(TestCase):

    def test_manager(self):

        root = URLPath.create_root()
        child = URLPath.create_article(root, "child")

        self.assertEqual(root.parent, None)
        self.assertEqual(list(root.children.active()), [child])
