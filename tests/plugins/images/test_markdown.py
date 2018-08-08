import base64
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from tests.base import RequireRootArticleMixin, TestBase
from wiki.core import markdown
from wiki.plugins.images import models


class ImageMarkdownTests(RequireRootArticleMixin, TestBase):
    def setUp(self):
        super().setUp()

        self.image_revision = models.ImageRevision(
            image=self._create_test_gif_file(), width=1, height=1
        )
        self.image = models.Image(article=self.root_article)
        self.image.add_revision(self.image_revision)
        self.assertEqual(1, self.image.id)

    def _create_test_gif_file(self):
        # A black 1x1 gif
        str_base64 = "R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs="
        filename = "test.gif"
        data = base64.b64decode(str_base64)
        filedata = BytesIO(data)
        return InMemoryUploadedFile(filedata, None, filename, "image", len(data), None)

    def test_before_and_after(self):
        md = markdown.ArticleMarkdown(article=self.root_article)
        md_text = md.convert("before [image:%s align:left] after" % self.image.id)
        before_pos = md_text.index("before")
        figure_pos = md_text.index("<figure")
        after_pos = md_text.index("after")
        self.assertTrue(before_pos < figure_pos < after_pos)

    def test_markdown(self):
        md = markdown.ArticleMarkdown(article=self.root_article)
        md_text = md.convert("[image:%s align:left]" % self.image.id)
        self.assertIn("<figure", md_text)
        self.assertNotIn("[image:%s align:left]" % self.image.id, md_text)
        md_text = md.convert("image: [image:%s align:left]\nadasd" % self.image.id)
        self.assertIn("<figure", md_text)
        self.assertIn("<figcaption", md_text)
        md_text = md.convert(
            "image: [image:%s align:right size:medium]\nadasd" % self.image.id
        )
        self.assertIn("<figure", md_text)
        self.assertIn("<figcaption", md_text)
        md_text = md.convert("image: [image:123 align:left size:medium]\nadasd")
        self.assertIn("Image not found", md_text)
        self.assertIn("<figcaption", md_text)

    def test_caption(self):
        md = markdown.ArticleMarkdown(article=self.root_article)
        md_text = md.convert(
            "[image:%s align:left]\n    this is visual" % self.image.id
        )
        self.assertIn("<figure", md_text)
        self.assertRegex(
            md_text, r'<figcaption class="caption">\s*this is visual\s*</figcaption>'
        )
        md = markdown.ArticleMarkdown(article=self.root_article)
        md_text = md.convert(
            "[image:%s align:left]\n    this is visual\n    second line" % self.image.id
        )
        self.assertIn("<figure", md_text)
        self.assertRegex(
            md_text,
            r'<figcaption class="caption">\s*this is visual\s*second line\s*</figcaption>',
        )

    def check_escape(self, text_to_escape):
        md = markdown.ArticleMarkdown(article=self.root_article)
        md_text = md.convert("`%s`" % text_to_escape)
        self.assertNotIn("<figure", md_text)
        self.assertIn(text_to_escape, md_text)

    def test_escape(self):
        self.check_escape("[image:%s align:left]" % self.image.id)
        self.check_escape("image tag: [image:%s]" % self.image.id)
