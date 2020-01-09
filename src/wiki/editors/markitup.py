from django import forms
from wiki.editors.base import BaseEditor


class MarkItUpWidget(forms.Widget):
    template_name = "wiki/forms/markitup.html"

    def __init__(self, attrs=None):
        # The 'rows' and 'cols' attributes are required for HTML correctness.
        default_attrs = {
            "class": "markItUp",
            "rows": "10",
            "cols": "40",
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class MarkItUpAdminWidget(MarkItUpWidget):
    """A simplified more fail-safe widget for the backend"""

    template_name = "wiki/forms/markitup-admin.html"


class MarkItUp(BaseEditor):
    editor_id = "markitup"

    def get_admin_widget(self, instance=None):
        return MarkItUpAdminWidget()

    def get_widget(self, instance=None):
        return MarkItUpWidget()

    class AdminMedia:
        css = {
            "all": (
                "wiki/markitup/skins/simple/style.css",
                "wiki/markitup/sets/admin/style.css",
            )
        }
        js = (
            "wiki/markitup/admin.init.js",
            "wiki/markitup/jquery.markitup.js",
            "wiki/markitup/sets/admin/set.js",
        )

    class Media:
        css = {
            "all": (
                "wiki/markitup/skins/simple/style.css",
                "wiki/markitup/sets/frontend/style.css",
            )
        }
        js = (
            "wiki/markitup/frontend.init.js",
            "wiki/markitup/jquery.markitup.js",
            "wiki/markitup/sets/frontend/set.js",
        )
