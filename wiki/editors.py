from conf import settings
from django.core.urlresolvers import get_callable

EditorClass = get_callable(settings.EDITOR)
editor = EditorClass()
