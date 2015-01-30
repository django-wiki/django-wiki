from __future__ import absolute_import
from wiki.conf import settings
from django.core.urlresolvers import get_callable

_EditorClass = None
_editor = None


def getEditorClass():
    global _EditorClass
    if not _EditorClass:
        _EditorClass = get_callable(settings.EDITOR)
    return _EditorClass


def getEditor():
    global _editor
    if not _editor:
        _editor = getEditorClass()()
    return _editor
