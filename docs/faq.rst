FAQ
===

Q: Why do I keep getting *"This slug conflicts with an existing URL."*
----------------------------------------------------------------------

A: When validating a slug, django-wiki will verify through
:doc:`settings`.``WIKI_CHECK_SLUG_URL_AVAILABLE`` (default: ``True``) that the URL is not
already occupied.

So if you keep getting an error that the "slug" isn't available, it's
probably because you left another URL pattern interfearing with django-wiki's
by letting your pattern (regexp) be too open. Forgetting a closing
``$`` is a common mistake.
