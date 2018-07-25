from tests.base import RequireRootArticleMixin, TestBase
from wiki.core import markdown


class RedlinksTests(RequireRootArticleMixin, TestBase):
    def test_internal(self):
        md = markdown.ArticleMarkdown(article=self.root_article)
        md_text = md.convert("[Internal](.)")
        self.assertIn("wiki-internal", md_text)
        self.assertNotIn("wiki-external", md_text)
        self.assertNotIn("wiki-broken", md_text)

    def test_external(self):
        md = markdown.ArticleMarkdown(article=self.root_article)
        md_text = md.convert("[External](/)")
        self.assertNotIn("wiki-internal", md_text)
        self.assertIn("wiki-external", md_text)
        self.assertNotIn("wiki-broken", md_text)

    def test_broken(self):
        md = markdown.ArticleMarkdown(article=self.root_article)
        md_text = md.convert("[Broken](broken)")
        self.assertNotIn("wiki-internal", md_text)
        self.assertNotIn("wiki-external", md_text)
        self.assertIn("wiki-broken", md_text)
