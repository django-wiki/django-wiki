from django.conf import settings as django_settings
from django.utils.translation import gettext

SLUG = "editsection"

#: Add "[edit]" links to all section headers till this level. By using
#: these links editing only the text from the selected section is possible.
MAX_LEVEL = getattr(django_settings, "WIKI_EDITSECTION_MAX_LEVEL", 3)

#: Text used for the section edit links which will appear next to section
#: headers. These links allow editing only the text of one particular section.
LINK_TEXT = getattr(django_settings, "WIKI_EDITSECTION_LINK_TEXT", gettext("[edit]"))
