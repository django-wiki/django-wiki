from django.conf import settings as django_settings

#: If a relative slug is used in a wiki markdown link and no article is
#: found with the given slug starting at the current articles level a
#: link to a not yet existing article is created. Creating the article
#: can be done by following the link. This link will be relative to
#: ``LOOKUP_LEVEL``. This should be the level that most articles are
#: created at.
LOOKUP_LEVEL = getattr(django_settings, "WIKI_LINKS_LOOKUP_LEVEL", 2)
