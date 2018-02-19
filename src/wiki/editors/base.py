from django import forms


class BaseEditor:

    """Editors should inherit from this. See wiki.editors for examples."""

    # The editor id can be used for conditional testing. If you write your
    # own editor class, you can use the same editor_id as some editor
    editor_id = 'plaintext'
    media_admin = ()
    media_frontend = ()

    def __init__(self, instance=None):
        self.instance = instance

    def get_admin_widget(self):
        return forms.Textarea()

    class AdminMedia:
        css = {}
        js = ()

    class Media:
        css = {}
        js = ()
