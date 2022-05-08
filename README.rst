django-wiki
===========

|Docs| |Build Status| |Coverage Status| |PyPi| |Downloads| |IRC|

.. |Docs| image:: https://readthedocs.org/projects/django-wiki/badge/?version=latest
   :target: https://django-wiki.readthedocs.io/
.. |Build status| image:: https://circleci.com/gh/django-wiki/django-wiki.svg?style=shield
   :target: https://circleci.com/gh/django-wiki/django-wiki
.. |Coverage Status| image:: https://codecov.io/github/django-wiki/django-wiki/coverage.svg?branch=master
   :target: https://codecov.io/github/django-wiki/django-wiki?branch=master
.. |PyPi| image:: https://badge.fury.io/py/wiki.svg
   :target: https://pypi.org/project/wiki/
.. |Downloads| image:: https://img.shields.io/pypi/dm/wiki.svg
   :target: https://pypi.org/project/wiki/
.. |IRC| image:: https://img.shields.io/badge/irc-%23django--wiki%20on%20libera.chat-blue.svg
   :target: https://webchat.freenode.net?channels=%23django-wiki

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

Django-wiki has almost fully translated into 12 languages, apart from the
default (English). But please help out in adding more languages! It's
very easy, you don't even need to be a programmer.

Some languages...

* Just need a little push, as they are almost fully complete
* Got initiatied and need a new instigator to carry on the ambitions
* Do not exist yet - but you can request them and become the coordinator.

`Visit the django-wiki project on Transifex <https://www.transifex.com/django-wiki/django-wiki/>`__

Demo
----

A demo running the latest ``master`` is available here, sign up for an
account to see the notification system, or you can log in with
user:``test`` and password:``test``.

https://demo.django-wiki.org

Community
---------

Please use our IRC or mailing list (google group) for getting in touch
on development and support. Please do not email developers asking for
personal support.

- #django-wiki on irc.freenode.net
- `django-wiki@googlegroups.com <https://groups.google.com/forum/#!forum/django-wiki>`__
- `twitter:djangowiki <https://twitter.com/djangowiki>`__

*THIS IS A WORK IN PROGRE...*
-----------------------------

Currently, the model API is subject to smaller changes, and the plugin
API seems pretty stable.

In order to customize the wiki, best idea is to override templates and create
your own template tags. Do not make your own hard copy of this repository in
order to fiddle with internal parts of the wiki -- this strategy will lead you
to lose out on future updates with highly improved features and plugins.
Possibly security updates as well!

The release cycle has already begun, so you can administer django-wiki
through Pypi and pip.

All views are class-based, however don't take it as an encouragement to
extend them, unless you are prepared to modify both templates and view
classes every time there is an update.

Contributing
------------

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
   for wiki", so we had to make up for that!
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


Requirements
------------

Please refer to current release to see exact version dependencies. And
make note that Pillow needs to have certain build dependencies satisfied
on your host system.

-  `Django <https://www.djangoproject.com>`__
-  `Markdown <https://github.com/waylan/Python-Markdown>`__
-  `django-mptt <https://github.com/django-mptt/django-mptt>`__
-  `django-sekizai <https://github.com/ojii/django-sekizai/>`__
-  `sorl-thumbnail <https://github.com/mariocesar/sorl-thumbnail>`__
-  `Pillow (Python Imaging Library) <https://pillow.readthedocs.io/en/latest/installation.html>`__
-  Python>=3.5


Docker tl;dr
------------

There is a docker container available here: https://github.com/riotkit-org/docker-django-wiki


Acknowledgements
----------------

-  The people at `edX <https://www.edx.org/>`__ & MIT for finding
   and supporting the project both financially and with ideas.
-  `django-cms <https://github.com/divio/django-cms>`__ for venturing
   where no django app has gone before in terms of well-planned features
   and high standards. It's a very big inspiration.
-  `django-mptt <https://github.com/django-mptt/django-mptt>`__, a
   wonderful utility for inexpensively using tree structures in Django
   with a relational database backend.
-  `spookylukey <https://github.com/spookylukey>`__,
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
