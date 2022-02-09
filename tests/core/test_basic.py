import tempfile
from datetime import datetime

from django.test import TestCase
from wiki.conf import settings as wiki_settings
from wiki.core.http import send_file
from wiki.forms import Group
from wiki.models import Article
from wiki.models import ArticleRevision
from wiki.models import URLPath

from ..base import wiki_override_settings
from ..testdata.models import CustomGroup


class URLPathTests(TestCase):
    def test_manager(self):

        root = URLPath.create_root()
        child = URLPath.create_urlpath(root, "child")

        self.assertIsNone(root.parent)
        self.assertEqual(list(root.children.all().active()), [child])


class CustomGroupTests(TestCase):
    @wiki_override_settings(WIKI_GROUP_MODEL="auth.Group")
    def test_setting(self):
        self.assertEqual(wiki_settings.GROUP_MODEL, "auth.Group")

    def test_custom(self):
        self.assertEqual(Group, CustomGroup)
        self.assertEqual(wiki_settings.GROUP_MODEL, "testdata.CustomGroup")


class LineEndingsTests(TestCase):
    def test_manager(self):

        article = Article()
        article.add_revision(
            ArticleRevision(title="Root", content="Hello\nworld"), save=True
        )
        self.assertEqual("Hello\r\nworld", article.current_revision.content)


class HttpTests(TestCase):
    def test_send_file(self):
        fabricate_request = self.client.get("/").wsgi_request
        fobject = tempfile.NamedTemporaryFile("r")
        response = send_file(fabricate_request, fobject.name, filename="test.pdf")
        assert response.has_header("Content-Disposition")
        assert "inline" in response.get("Content-Disposition")
        response = send_file(fabricate_request, fobject.name, filename="test.jpeg")
        assert response.has_header("Content-Disposition")
        response = send_file(
            fabricate_request,
            fobject.name,
            filename="test.jpeg",
            last_modified=datetime.now(),
        )
        assert response.has_header("Content-Disposition")
        fobject.close()
