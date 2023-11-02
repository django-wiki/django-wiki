import re

from django.urls import reverse
from django_functest import FuncBaseMixin
from wiki.models import URLPath

from ...base import DjangoClientTestBase
from ...base import RequireRootArticleMixin
from ...base import WebTestBase

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


TEST_CONTENT_SRC_COMMENT = """
# Section 1
Section 1 Lorem ipsum dolor sit amet

```python
# hello world
print("hello world")
```

# Section 2
Section 2 Lorem ipsum dolor sit amet
"""


class EditSectionTests(RequireRootArticleMixin, DjangoClientTestBase):
    def test_editsection(self):
        # Test creating links to allow editing all sections individually
        urlpath = URLPath.create_urlpath(
            URLPath.root(), "testedit", title="TestEdit", content=TEST_CONTENT
        )
        output = urlpath.article.render()
        expected = (
            r"(?s)"
            r'Title 1<a class="article-edit-title-link" href="/testedit/_plugin/editsection/header/wiki-toc-title-1/">\[edit\]</a>.*'
            r'Title 2<a class="article-edit-title-link" href="/testedit/_plugin/editsection/header/wiki-toc-title-2/">\[edit\]</a>.*'
            r'Title 3<a class="article-edit-title-link" href="/testedit/_plugin/editsection/header/wiki-toc-title-3/">\[edit\]</a>.*'
            r'Title 4<a class="article-edit-title-link" href="/testedit/_plugin/editsection/header/wiki-toc-title-4/">\[edit\]</a>.*'
            r'Title 5<a class="article-edit-title-link" href="/testedit/_plugin/editsection/header/wiki-toc-title-5/">\[edit\]</a>.*'
            r'Title 6<a class="article-edit-title-link" href="/testedit/_plugin/editsection/header/wiki-toc-title-6/">\[edit\]</a>.*'
        )
        self.assertRegex(output, expected)

        # Test wrong header text. Editing should fail with a redirect.
        url = reverse(
            "wiki:editsection",
            kwargs={"path": "testedit/", "header": "does-not-exist"},
        )
        response = self.client.get(url)
        self.assertRedirects(
            response, reverse("wiki:get", kwargs={"path": "testedit/"})
        )

        # Test extracting sections for editing
        url = reverse(
            "wiki:editsection",
            kwargs={"path": "testedit/", "header": "wiki-toc-title-4"},
        )
        response = self.client.get(url)
        expected = ">### Title 4[\r\n]*" "<"
        self.assertRegex(response.rendered_content, expected)

        url = reverse(
            "wiki:editsection",
            kwargs={"path": "testedit/", "header": "wiki-toc-title-3"},
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

    def test_broken_content(self):
        # Regression test for https://github.com/django-wiki/django-wiki/issues/1094
        TEST_CONTENT = "### [Here we go](#anchor)"
        urlpath = URLPath.create_urlpath(
            URLPath.root(), "testedit", title="TestEdit", content=TEST_CONTENT
        )
        output = urlpath.article.render()
        print(output)

    def get_section_content(self, response):
        # extract actual section content from response (editor)
        m = re.search(
            r"<textarea[^>]+>(?P<content>[^<]+)</textarea>",
            response.rendered_content,
            re.DOTALL,
        )
        if m:
            return m.group("content")
        else:
            return ""

    def test_sourceblock_with_comment(self):
        # https://github.com/django-wiki/django-wiki/issues/1246
        URLPath.create_urlpath(
            URLPath.root(),
            "testedit_src",
            title="TestEditSourceComment",
            content=TEST_CONTENT_SRC_COMMENT,
        )
        url = reverse(
            "wiki:editsection",
            kwargs={"path": "testedit_src/", "header": "wiki-toc-section-2"},
        )
        response = self.client.get(url)
        actual = self.get_section_content(response)
        expected = "# Section 2\r\nSection 2 Lorem ipsum dolor sit amet\r\n"
        self.assertEqual(actual, expected)

    def test_nonunique_headers(self):
        """test whether non-unique headers will be handled properly"""
        source = """# Investigation 1\n\n## Date\n2023-01-01\n\n# Investigation 2\n\n## Date\n2023-01-02"""
        URLPath.create_urlpath(
            URLPath.root(),
            "testedit_src",
            title="TestEditSourceComment",
            content=source,
        )
        url = reverse(
            "wiki:editsection",
            kwargs={"path": "testedit_src/", "header": "wiki-toc-date"},
        )
        response = self.client.get(url)
        actual = self.get_section_content(response)
        expected = "## Date\r\n2023-01-01\r\n\r\n"

        self.assertEqual(actual, expected)
        url = reverse(
            "wiki:editsection",
            kwargs={"path": "testedit_src/", "header": "wiki-toc-date_1"},
        )
        response = self.client.get(url)
        actual = self.get_section_content(response)
        expected = "## Date\r\n2023-01-02"
        self.assertEqual(actual, expected)

    def test_underscore_and_dot(self):
        """test whether we can handle non-slug characters like dots in header IDs"""
        # Explanation: While autogenerated ids are slugified, Markdown allows to manually
        # specify the ID using the {#custom_id_value} syntax. As HTML5 only requires ID
        # values not to contain whitespace, we should be able to handle any valid HTML5 ID, too.
        source = """# Title 1 {#some_id_with.dot}\n\n"""
        urlpath = URLPath.create_urlpath(
            URLPath.root(), "testedit", title="TestEdit", content=source
        )
        # rendering causes NoReverseMatch without the fix
        actual = urlpath.article.render()
        expected = '<h1 id="some_id_with.dot">Title 1<a class="article-edit-title-link" href="/testedit/_plugin/editsection/header/some_id_with.dot/">[edit]</a></h1>'
        self.assertEqual(actual, expected)


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
                kwargs={"path": "testedit/", "header": "wiki-toc-title-3"},
            )
        )
        self.fill({"#id_content": "# Header 1\nContent of the new section"})
        self.submit("#id_save")
        expected = (
            r"(?s)"
            r'Title 1<a class="article-edit-title-link" href="/testedit/_plugin/editsection/header/wiki-toc-title-1/">\[edit\]</a>.*'
            r'Title 2<a class="article-edit-title-link" href="/testedit/_plugin/editsection/header/wiki-toc-title-2/">\[edit\]</a>.*'
            r'Header 1<a class="article-edit-title-link" href="/testedit/_plugin/editsection/header/wiki-toc-header-1/">\[edit\]</a>.*'
            r"Content of the new section.*"
            r'Title 5<a class="article-edit-title-link" href="/testedit/_plugin/editsection/header/wiki-toc-title-5/">\[edit\]</a>.*'
            r'Title 6<a class="article-edit-title-link" href="/testedit/_plugin/editsection/header/wiki-toc-title-6/">\[edit\]</a>.*'
        )
        self.assertRegex(self.last_response.content.decode("utf-8"), expected)

        new_number = URLPath.objects.get(
            slug="testedit"
        ).article.current_revision.revision_number
        self.assertEqual(new_number, old_number + 1)
