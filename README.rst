django-wiki
===========

|Docs| |Build Status| |Coverage Status| |PyPi| |Downloads| |IRC|

.. |Docs| image:: https://readthedocs.org/projects/django-wiki/badge/?version=latest
   :target: https://django-wiki.readthedocs.io/
.. |Build status| image:: https://circleci.com/gh/django-wiki/django-wiki.svg?style=shield
   :target: https://circleci.com/gh/django-wiki/django-wiki
.. |Coverage Status| image:: https://codecov.io/github/django-wiki/django-wiki/coverage.svg?branch=main
   :target: https://codecov.io/github/django-wiki/django-wiki?branch=main
.. |PyPi| image:: https://badge.fury.io/py/wiki.svg
   :target: https://pypi.org/project/wiki/
.. |Downloads| image:: https://img.shields.io/pypi/dm/wiki.svg
   :target: https://pypi.org/project/wiki/
.. |IRC| image:: https://img.shields.io/badge/irc-%23django--wiki%20on%20libera.chat-blue.svg
   :target: https://web.libera.chat/?channel=#django-wiki

Django support
--------------

The below table explains which Django versions are supported.

+------------------+----------------+--------------+
| Release          | Django         | Upgrade from |
+==================+================+==============+
| 0.9.x            | 2.2, 3.0, 3.1, | 0.7          |
|                  | 3.2, 4.0       |              |
+------------------+----------------+--------------+
| 0.8.x            | 2.2, 3.0, 3.1, | 0.7          |
|                  | 3.2, 4.0       |              |
+------------------+----------------+--------------+
| 0.7.x            | 2.2, 3.0, 3.1, | 0.5 or 0.6   |
|                  | 3.2            |              |
+------------------+----------------+--------------+
| 0.6.x            | 2.1, 2.2, 3.0  | 0.5          |
+------------------+----------------+--------------+
| 0.5.x            | 2.1, 2.2       | 0.4          |
+------------------+----------------+--------------+
| 0.4.x            | 1.11, 2.0, 2.1 | 0.3          |
+------------------+----------------+--------------+
| 0.3.x            | 1.8, 1.9,      | 0.2          |
|                  | 1.10, 1.11     |              |
+------------------+----------------+--------------+
| 0.2.x            | 1.8, 1.9, 1.10 | 0.1          |
+------------------+----------------+--------------+
| 0.1.x            | 1.5, 1.6, 1.7  | 0.0.24       |
+------------------+----------------+--------------+
| 0.0.24           | 1.4, 1.5, 1.6  | 0.0.?        |
|                  | 1.7 (unstable) |              |
+------------------+----------------+--------------+

For upgrade instructions, please refer to the `Release
Notes <https://django-wiki.readthedocs.io/en/latest/release_notes.html>`__


Translations (Transifex)
------------------------

Django-wiki is fully translated into 13 languages, apart from the
default (English) and some additional languages underway.

But please help out in adding more languages!
It's very easy and you don't even need to be a programmer.

Some languages...

* ...just need a little push, as they are almost fully complete
* ...got initiated and need a new instigator to carry on the ambitions
* ...do not exist yet - but you can request them and become the coordinator

`Visit the django-wiki project on Transifex <https://www.transifex.com/django-wiki/django-wiki/>`__

Demo
----

A demo running the latest ``main`` branch is available here:

https://demo.django-wiki.org

Sign up for an account to see the notification system,
or you can log in with the existing account:

- user: ``admin``
- password:``admin``

Community
---------

Please use our IRC or mailing list (google group) for getting in touch
on development and support. Please do not email developers asking for
personal support.

- Discussions on GitHub: `<https://github.com/django-wiki/django-wiki/discussions>`__
- `#django-wiki on libera.chat <https://web.libera.chat/?channel=#django-wiki>`__
- `django-wiki@googlegroups.com <https://groups.google.com/forum/#!forum/django-wiki>`__
- `twitter:djangowiki <https://twitter.com/djangowiki>`__

*Always a work in progr...*
-----------------------------

On a number of factors,
this project has proven itself useful and stable.

- There won't be changes that are expected to cause loss of data without a proper upgrade path.
- The model API has been very stable and is only subject to smaller changes.
- The plugin API seems pretty stable.
- You can maintain the latest version of django-wiki through PyPi (package name: ``wiki``), using `SemVer <https://semver.org/>`__ versioning schema.

What should I customize? What can break?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You will need to learn a bit of Django to customize django-wiki.

The simplest is to override templates and create your own template tags.
Do not make your own hard copy of this repository in order to fiddle with internal parts of the wiki,
this strategy will lead you to lose out on future updates with highly improved features, plugins and security fixes.

You can also override the whole Bootstrap theming.
At present,
you're best off maintaining your own Bootstrap SCSS and hard-copying, then overriding django-wiki's rules.

All Python views are class-based.
However for most cases overriding views and URLs shouldn't be the best place to start
since most customization can be achieved through plugins, templates and SCSS.

Contributing
------------

Contributions are welcome! ❤️

Please read our
`Developer Guide <https://django-wiki.readthedocs.io/en/latest/development/index.html>`__

Manifesto
---------

Django needs a mature wiki system appealing to all kinds of needs, both
big and small:

-  **Be pluggable and light-weight.** Don't integrate optional features
   in the core.
-  **Be open.** Make an extension API that allows the ecology of the
   wiki to grow in a structured way. Wikipedia consists of over `1100
   extension projects <https://phabricator.wikimedia.org/diffusion/query/all/?after=1100>`__
   written for MediaWiki. We should learn from this.
-  **Be smart.** `This
   is <https://upload.wikimedia.org/wikipedia/commons/f/f7/MediaWiki_1.24.1_database_schema.svg>`__
   the map of tables in MediaWiki - we'll understand the choices of
   other wiki projects and make our own. After-all, this is a Django
   project.
-  **Be simple.** The source code should *almost* explain itself.
-  **Be structured.** Markdown is a simple syntax for readability.
   Features should be implemented either through easy coding patterns in
   the content field, but rather stored in a structured way (in the
   database) and managed through a friendly interface. This gives
   control back to the website developer, and makes knowledge more
   usable. Just ask: Why has Wikipedia never changed? Answer: Because
   it's knowledge is stored in a complicated way, thus it becomes very
   static.

Docs
----

See the docs/ folder, or read them at:

https://django-wiki.readthedocs.io/en/latest/

If you wish to add something, please ask in the google group or raise an
issue if you're in doubt about whether something might change.

Background
----------

Django-wiki is a rewrite of
`django-simplewiki <https://code.google.com/p/django-simple-wiki/>`__, a
project from 2009 that aimed to be a base system for a wiki. It proposed
that the user should customize the wiki by overwriting templates, but
soon learned that the only customization that really took place was that
people forked the entire project. We don't want that for django-wiki, we
want it to be modular and extendable.

As of now, Django has existed for too long without a proper wiki
application. The dream of django-wiki is to become a contestant
alongside Mediawiki, so that Django developers can stick to the Django
platform even when facing tough challenges such as implementing a wiki.


Q&A
---

-  **Why is the module named just** ``wiki`` **?** Because when we tried
   ``pip install wiki``, it returned "No distributions at all found
   for wiki", so we had to make up for that! ...oh, and django-wiki was occupied.
-  **What markup language will you use?**
   `Markdown <https://pypi.python.org/pypi/Markdown>`__. The markup
   renderer is not a pluggable part but has been internalized into core
   parts. Discussion should go here:
   https://github.com/django-wiki/django-wiki/issues/76
-  **Why not use django-reversion?** It's a great project, but if the
   wiki has to grow ambitious, someone will have to optimize its
   behavior, and using a third-party application for something as
   crucial as the revision system is a no-go in this regard.
-  **Any support for multiple wikis?** Yes, in an sense you can just
   imagine that you always have multiple wikis, because you always have
   hierarchies and full control of their permissions. See this
   discussion: https://github.com/django-wiki/django-wiki/issues/63


Docker tl;dr
------------

There is a docker container available here: https://github.com/riotkit-org/docker-django-wiki


Acknowledgements
----------------

-  The people at `edX <https://www.edx.org/>`__ & MIT for finding
   and supporting the project both financially and with ideas.
-  `django-mptt <https://github.com/django-mptt/django-mptt>`__, a
   wonderful utility for inexpensively using tree structures in Django
   with a relational database backend.
-  `oscarmcm <https://github.com/oscarmcm>`__,
   `atombrella <https://github.com/atombrella>`__,
   `floemker <https://github.com/floemker>`__,
   `rsalmaso <https://github.com/rsalmaso>`__,
   `spookylukey <https://github.com/spookylukey>`__,
   `jluttine <https://github.com/jluttine>`__,
   `duvholt <https://github.com/duvholt>`__,
   `valberg <https://github.com/valberg>`__,
   `jdcaballerov <https://github.com/jdcaballerov>`__,
   `yekibud <https://github.com/yekibud>`__,
   `bridger <https://github.com/bridger>`__,
   `TomLottermann <https://github.com/TomLottermann>`__,
   `crazyzubr <https://github.com/crazyzubr>`__, and `everyone
   else <https://github.com/django-wiki/django-wiki/graphs/contributors>`__
   involved!

Original source of inspiration back in 2009 was django-cms,
and since then Wagtail has also done a tremendous amount of work to promote Django models as a fundamental structure and enabler for application design.
