django-wiki
===========

|Docs| |Build Status| |Coverage Status| |PyPi| |Dependency Status|

.. |Docs| image:: https://readthedocs.org/projects/django-wiki/badge/?version=latest
   :target: http://django-wiki.readthedocs.io/
.. |Build Status| image:: https://travis-ci.org/django-wiki/django-wiki.png?branch=master
   :target: https://travis-ci.org/django-wiki/django-wiki
.. |Coverage Status| image:: https://codecov.io/github/django-wiki/django-wiki/coverage.svg?branch=master
   :target: https://codecov.io/github/django-wiki/django-wiki?branch=master
.. |PyPi| image:: https://badge.fury.io/py/wiki.svg
   :target: https://pypi.python.org/pypi/wiki/
.. |Downloads| image:: https://img.shields.io/pypi/dm/wiki.svg
   :target: https://pypi.python.org/pypi/wiki/
.. |Dependency Status| image:: https://gemnasium.com/django-wiki/django-wiki.svg
   :target: https://gemnasium.com/django-wiki/django-wiki


Django support
--------------

The below table explains which Django versions are supported.

+------------+----------------+--------------+
| Release    | Django         | Upgrade from |
+============+================+==============+
| 0.2        | 1.8, 1.9, 1.10 | 0.1          |
+------------+----------------+--------------+
| 0.1        | 1.5, 1.6, 1.7  | 0.24         |
+------------+----------------+--------------+
| 0.24       | 1.4, 1.5, 1.6  | -            |
|            | 1.7 (unstable) |              |
+------------+----------------+--------------+

For upgrade instructions, please refer to the `Release
Notes <http://django-wiki.readthedocs.io/en/latest/release_notes.html>`__


News
----

October 13, 2016
~~~~~~~~~~~~~~~~

0.2b1 released: `Release notes <http://django-wiki.readthedocs.io/en/latest/release_notes.html#django-wiki-0-2-dev>`__

June 19, 2016
~~~~~~~~~~~~~

0.1.2 released: `Release notes <http://django-wiki.readthedocs.io/en/latest/release_notes.html#django-wiki-0-1-2>`__

May 6, 2016
~~~~~~~~~~~

0.1.1 released: `Release notes <http://django-wiki.readthedocs.io/en/latest/release_notes.html#django-wiki-0-1-1>`__


January 25, 2016
~~~~~~~~~~~~~~~~

0.1 final released


December 26th, 2015
~~~~~~~~~~~~~~~~~~~

A new release 0.0.24.4 is out and has fixes for the Django ``loaddata`` management command such that you can create dumps and restore the dump. Notice, though, that ``loaddata`` only works for Django 1.7+.

Django 1.9 support is available in the current master, please help get a 0.1 released by giving feed back in the last remaining issues:

https://github.com/django-wiki/django-wiki/milestones/0.1


November 16th, 2015
~~~~~~~~~~~~~~~~~~~

Django 1.8 support is very ready and 0.1 is right on the doorstep now.


January 26th, 2015
~~~~~~~~~~~~~~~~~~

After too long, the new release is out.

The wait was mainly due to all the confusing changes by adding support
of Python 3 and readying the migrations for Django 1.7. But there's
actually new features, too.

-  Bootstrap 3.3.1 and Font Awesome 4 (Christian Duvholt)
-  ``django_nyt`` instead of builtin ``django_notify`` (Benjamin Bach,
   Maximilien Cuony)
-  ``tox`` for testing (Luke Plant)
-  Appropriate use of gettext\_lazy (Jaakko Luttinen)
-  Fixed support of custom username fields (Jan De Bleser)
-  Several fixes to the attachment plugin (Christian Duvholt)
-  Errors on notifications settings tab (Benjamin Richter)
-  Chinese translations (Ronald Bai)
-  Finish translations (Jaakko Luttinen)
-  Compatibility with custom user model in article settings (Andy Fang)
-  Fixed bug when ``[attachment:XX]`` present multiple times on same
   line (Maximilien Cuony)
-  Simple mediawiki import management command (Maximilien Cuony)
-  Python 3 and Django 1.6 compatibility (Russell-Jones, Antonin
   Lenfant, Luke Plant, Lubimov Igor, Benjamin Bach)
-  (and more, forgiveness asked if anyone feels left out)


Translations (Transifex)
------------------------

Django-wiki has almost fully translated into 7 languages, apart from the
default (English). But please help out in adding more languages! It's
very easy, you don't even need to be a programmer.

https://www.transifex.com/django-wiki/django-wiki/

Demo
----

A demo running the latest ``master`` is available here, sign up for an
account to see the notification system.

https://demo.django.wiki

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

South is used so no database changes will cause data loss. In order to
customize the wiki, best idea is to override templates and create your
own template tags. Do not make your own hard copy of this repository in
order to fiddle with internal parts of the wiki -- this strategy will
lead you to lose out on future updates with highly improved features
and plugins. Possibly security updates as well!

The release cycle has already begun, so you can administer django-wiki
through Pypi and pip.

All views are class-based, however don't take it as an encouragement to
extend them, unless you are prepared to modify both templates and view
classes every time there is an update.

Contributing
------------

The best way to contribute is to use our Github issue list to look
at current wishes. The list is found here:

https://github.com/django-wiki/django-wiki/issues/

Generally speaking, we need more **unit tests**, and new
features will not be accepted without tests. To add more stuff the
the project without tests wouldn't be fair to the project or
your hard work. We use coverage metrics to see that each new
contribution does not significantly impact test coverage.

The easiest way to add features is to write a plugin. Please create an
issue to discuss whether your plugin idea is a core plugin
(``wiki.plugins.*``) or external plugin. If there are additions needed
to the plugin API, we can discuss that as well!

To run django-wiki's tests, run ``make test``
after installing the requirements.

If you want to test for more **environments**, install "tox"
(``pip install tox``) and then just run ``tox`` to run the test
suite on multiple environments.

To run **specific tests**, call ``pytest`` with a path to the file with
the tests you wish to run, for instance ``pytest wiki/tests/test_views.py``.

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

http://django-wiki.readthedocs.io/en/latest/

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
-  Python>=2.7 or Python>=3.2


Development
-----------

The folder **testproject/** contains a pre-configured django project and
an sqlite database. Login for django admin is *admin:admin*. This
project should always be maintained, but please do not commit changes to
the SQLite database as we only care about its contents in case data
models are changed.


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

