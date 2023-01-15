import wiki.editors
from django.forms import Textarea
from wiki.editors.base import BaseEditor

from ..base import RequireRootArticleMixin
from ..base import WebTestBase
from ..base import wiki_override_settings


class CustomEditor(BaseEditor):
    def get_widget(self, revision=None):
        return Textarea(attrs={"data-revision": revision.pk})

    def get_admin_widget(self, revision=None):
        return Textarea(attrs={"data-revision": revision.pk})


class EditorTest(RequireRootArticleMixin, WebTestBase):
    def setUp(self):
        super().setUp()
        # reset the cached editor class and instance
        wiki.editors._editor, wiki.editors._EditorClass = None, None

    def test_editor_widget_markitup(self):
        response = self.get_url("wiki:edit", path="")
        self.assertContains(
            response,
            '<textarea name="content" class="markItUp" rows="10" cols="40" id="id_content">',
        )

    def test_admin_widget_markitup(self):
        response = self.get_url(
            "admin:wiki_articlerevision_change",
            object_id=self.root_article.current_revision.id,
        )
        self.assertContains(
            response,
            '<textarea name="content" class="markItUp" rows="10" cols="40" id="id_content">',
        )

    @wiki_override_settings(WIKI_EDITOR="wiki.editors.base.BaseEditor")
    def test_editor_widget_base(self):
        response = self.get_url("wiki:edit", path="")
        self.assertContains(
            response, '<textarea name="content" cols="40" rows="10" id="id_content">'
        )

    @wiki_override_settings(WIKI_EDITOR="wiki.editors.base.BaseEditor")
    def test_admin_widget_base(self):
        response = self.get_url(
            "admin:wiki_articlerevision_change",
            object_id=self.root_article.current_revision.id,
        )
        self.assertContains(
            response, '<textarea name="content" cols="40" rows="10" id="id_content">'
        )

    @wiki_override_settings(WIKI_EDITOR="tests.core.test_editor.CustomEditor")
    def test_editor_widget_custom(self):
        response = self.get_url("wiki:edit", path="")
        self.assertContains(
            response,
            '<textarea name="content" cols="40" rows="10" data-revision="{}" id="id_content">'.format(
                self.root_article.current_revision.id
            ),
        )

    @wiki_override_settings(WIKI_EDITOR="tests.core.test_editor.CustomEditor")
    def test_admin_widget_custom(self):
        response = self.get_url(
            "admin:wiki_articlerevision_change",
            object_id=self.root_article.current_revision.id,
        )
        self.assertContains(
            response,
            '<textarea name="content" cols="40" rows="10" data-revision="{}" id="id_content">'.format(
                self.root_article.current_revision.id
            ),
        )
