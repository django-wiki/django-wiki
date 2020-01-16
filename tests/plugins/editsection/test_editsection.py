from django.urls import reverse
from django_functest import FuncBaseMixin
from wiki.models import URLPath

from ...base import DjangoClientTestBase, RequireRootArticleMixin, WebTestBase

TEST_CONTENT = (
    "Title 1\n"
    "=======\n"
    "## Title 2\n"
    "Title 3\n"
    "-------\n"
    "a\n"
    "Paragraph\n"
    "-------\n"
    "### Title 4\n"
    "## Title 5\n"
    "# Title 6\n"
)


class EditSectionTests(RequireRootArticleMixin, DjangoClientTestBase):
    def test_editsection(self):
        # Test creating links to allow editing all sections individually
        urlpath = URLPath.create_urlpath(
            URLPath.root(), "testedit", title="TestEdit", content=TEST_CONTENT
        )
        output = urlpath.article.render()
        expected = (
            r"(?s)"
            r'Title 1<a class="article-edit-title-link" href="/testedit/_plugin/editsection/1-0-0/header/T1/">\[edit\]</a>.*'
            r'Title 2<a class="article-edit-title-link" href="/testedit/_plugin/editsection/1-1-0/header/T2/">\[edit\]</a>.*'
            r'Title 3<a class="article-edit-title-link" href="/testedit/_plugin/editsection/1-2-0/header/T3/">\[edit\]</a>.*'
            r'Title 4<a class="article-edit-title-link" href="/testedit/_plugin/editsection/1-2-1/header/T4/">\[edit\]</a>.*'
            r'Title 5<a class="article-edit-title-link" href="/testedit/_plugin/editsection/1-3-0/header/T5/">\[edit\]</a>.*'
            r'Title 6<a class="article-edit-title-link" href="/testedit/_plugin/editsection/2-0-0/header/T6/">\[edit\]</a>.*'
        )
        self.assertRegex(output, expected)

        # Test wrong header text. Editing should fail with a redirect.
        url = reverse(
            "wiki:editsection",
            kwargs={"path": "testedit/", "location": "1-2-1", "header": "Test"},
        )
        response = self.client.get(url)
        self.assertRedirects(
            response, reverse("wiki:get", kwargs={"path": "testedit/"})
        )

        # Test extracting sections for editing
        url = reverse(
            "wiki:editsection",
            kwargs={"path": "testedit/", "location": "1-2-1", "header": "T4"},
        )
        response = self.client.get(url)
        expected = ">### Title 4[\r\n]*" "<"
        self.assertRegex(response.rendered_content, expected)

        url = reverse(
            "wiki:editsection",
            kwargs={"path": "testedit/", "location": "1-2-0", "header": "T3"},
        )
        response = self.client.get(url)
        expected = (
            ">Title 3[\r\n]*"
            "-------[\r\n]*"
            "a[\r\n]*"
            "Paragraph[\r\n]*"
            "-------[\r\n]*"
            "### Title 4[\r\n]*"
            "<"
        )
        self.assertRegex(response.rendered_content, expected)


class EditSectionEditBase(RequireRootArticleMixin, FuncBaseMixin):
    pass


class EditSectionEditTests(EditSectionEditBase, WebTestBase):
    # Test editing a section
    def test_editsection_edit(self):
        urlpath = URLPath.create_urlpath(
            URLPath.root(), "testedit", title="TestEdit", content=TEST_CONTENT
        )
        old_number = urlpath.article.current_revision.revision_number

        self.get_literal_url(
            reverse(
                "wiki:editsection",
                kwargs={"path": "testedit/", "location": "1-2-0", "header": "T3"},
            )
        )
        self.fill({"#id_content": "# Header 1\nContent of the new section"})
        self.submit("#id_save")
        expected = (
            r"(?s)"
            r'Title 1<a class="article-edit-title-link" href="/testedit/_plugin/editsection/1-0-0/header/T1/">\[edit\]</a>.*'
            r'Title 2<a class="article-edit-title-link" href="/testedit/_plugin/editsection/1-1-0/header/T2/">\[edit\]</a>.*'
            r'Header 1<a class="article-edit-title-link" href="/testedit/_plugin/editsection/2-0-0/header/H1/">\[edit\]</a>.*'
            r"Content of the new section.*"
            r'Title 5<a class="article-edit-title-link" href="/testedit/_plugin/editsection/2-1-0/header/T5/">\[edit\]</a>.*'
            r'Title 6<a class="article-edit-title-link" href="/testedit/_plugin/editsection/3-0-0/header/T6/">\[edit\]</a>.*'
        )
        self.assertRegex(self.last_response.content.decode("utf-8"), expected)

        new_number = URLPath.objects.get(
            slug="testedit"
        ).article.current_revision.revision_number
        self.assertEqual(new_number, old_number + 1)
