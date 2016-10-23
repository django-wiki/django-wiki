FAQ
===

Q: Why can't I move articles?
-----------------------------

A: Moving articles is not trivial. Here are a couple of reasons:

 * Other articles may link to them.
 * Permissions may change if you move the articles into a different hierarchy
 * We keep revisions of stuff, so the action of moving an article will create a new revision.
 * ...but what if the revision is reverted and we had automatically renamed stuff?

Because it isn't trivial to move articles, the work has delayed somewhat.

Resources:

 * `Pull Request #461 <https://github.com/django-wiki/django-wiki/pull/461>`__
 * `Issue #154 <https://github.com/django-wiki/django-wiki/issues/154>`__


Q: Why do I keep getting *"This slug conflicts with an existing URL."*
----------------------------------------------------------------------

A: When validating a slug, django-wiki will verify through
:doc:`../settings`.``WIKI_CHECK_SLUG_URL_AVAILABLE`` (default: ``True``) that the URL is not
already occupied.

So if you keep getting an error that the "slug" isn't available, it's
probably because you left another URL pattern interfearing with django-wiki's
by letting your pattern (regexp) be too open. Forgetting a closing
``$`` is a common mistake.
