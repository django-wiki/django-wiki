django-wiki
===========

Important notice
----------------

Version **0.0.24** is now out and is the final release before **0.1** in which
migrations will be reset.

**0.0.24** adds Django 1.7 support, however it's not well-tested.

**0.1** (available as current master branch) adds Django 1.7 and 1.8 support, working as of now!

Please refer to the [Release Notes](http://django-wiki.readthedocs.org/en/latest/release_notes.html#django-wiki-0-0-24)

Changes underway
----------------

 - [x] Migrations reset
 - [x] Django 1.7 support
 - [x] Django 1.8 support
 - [x] pep8 the whole codebase #287
 - [x] Transifex
 - [ ] Distribution with Wheels

News
----

***News: January 26th, 2015***

After too long, the new release is out.

The wait was mainly due to all the confusing changes by adding support of Python 3
and readying the migrations for Django 1.7. But there's actually new features, too.

 - Bootstrap 3.3.1 and Font Awesome 4 (Christian Duvholt)
 - `django_nyt` instead of builtin `django_notify` (Benjamin Bach, Maximilien Cuony)
 - `tox` for testing (Luke Plant)
 - Appropriate use of gettext_lazy (Jaakko Luttinen)
 - Fixed support of custom username fields (Jan De Bleser)
 - Several fixes to the attachment plugin (Christian Duvholt)
 - Errors on notifications settings tab (Benjamin Richter)
 - Chinese translations (Ronald Bai)
 - Finish translations (Jaakko Luttinen)
 - Compatibility with custom user model in article settings (Andy Fang)
 - Fixed bug when `[attachment:XX]` present multiple times on same line (Maximilien Cuony)
 - Simple mediawiki import management command (Maximilien Cuony)
 - Python 3 and Django 1.6 compatibility (Russell-Jones, Antonin Lenfant, Luke Plant, Lubimov Igor, Benjamin Bach)
 - (and more, forgiveness asked if anyone feels left out)


Translations (Transifex)
------------------------

Django-wiki has almost fully translated into 7 languages, apart from the default (English). But please help out in adding more languages! It's very easy, you don't even need to be a programmer.

https://www.transifex.com/projects/p/django-wiki/

Demo
----

A demo is available here, sign up for an account to see the notification system.

[http://demo.django-wiki.org/](http://demo.django-wiki.org/)

Community
---------

Please use our IRC or mailing list (google group) for getting in touch on development and support. Please do not email developers asking for personal support.

- \#django-wiki on irc.freenode.net
- [django-wiki@googlegroups.com](https://groups.google.com/d/forum/django-wiki)
- [twitter:djangowiki](https://twitter.com/djangowiki)

*THIS IS A WORK IN PROGRE...*
---------------------------------

Currently, the model API is subject to smaller changes, and the plugin API seems pretty stable.

South is used so no database changes will cause data loss. In order to customize the wiki, best idea is to override templates and create your own template tags. Do not make your own hard copy of this repository in order to fiddle with internal parts of the wiki -- this strategy will lead you to loose out on future updates with highly improved features and plugins. Possibly security updates as well!

The release cycle has already begun, so you can administer django-wiki through Pypi and pip.

All views are class-based, however don't take it as an encouragement to extend them, unless you are prepared to modify both templates and view classes every time there is an update.

Contributing
------------

[TODO](https://github.com/benjaoming/django-wiki/blob/master/TODO.md) contains an overview of features planned or under development.

Consider any moment in life that you could have been writing **unit tests** for django-wiki.

The easiest way to add features is to write a plugin. Please create an issue to discuss whether your plugin idea is a core plugin (`wiki.plugins.*`) or external plugin. If there are additions needed to the plugin API, we can discuss that as well!

To run the tests, run "python runtests.py" after installing the requirements. Better, install "tox" (using "pip install tox") and then just run "tox" to run the test suite on multiple environments.

To run specific tests, call runtests.py with the arguments that you would pass to the normal "manage.py test" command.


Manifesto
---------

Django needs a mature wiki system appealing to all kinds of needs, both big and small:

 * **Be pluggable and light-weight.** Don't integrate optional features in the core.
 * **Be open.** Make an extension API that allows the ecology of the wiki to grow. After all, Wikipedia consists of some [680 extensions](http://svn.wikimedia.org/viewvc/mediawiki/trunk/extensions/) written for MediaWiki.
 * **Be smart.** [This is](https://upload.wikimedia.org/wikipedia/commons/8/88/MediaWiki_database_schema_1-19_%28r102798%29.png) the map of tables in MediaWiki - we'll understand the choices of other wiki projects and make our own. After-all, this is a Django project.
 * **Be simple.** The source code should *almost* explain itself.
 * **Be structured.** Markdown is a simple syntax for readability. Features should be implemented either through easy coding patterns in the content field, but rather stored in a structured way (in the database) and managed through a friendly interface. This gives control back to the website developer, and makes knowledge more usable. Just ask: Why has Wikipedia never changed? Answer: Because it's knowledge is stored in a complicated way, thus it becomes very static.

Docs
----

See the docs/ folder, or read them at:

http://django-wiki.readthedocs.org/en/latest/

If you wish to add something, please ask in the google group or raise an issue
if you're in doubt about whether something might change.

Background
----------

Django-wiki is a rewrite of [django-simplewiki](http://code.google.com/p/django-simple-wiki/), a project from 2009 that aimed to be a base system for a wiki. It proposed that the user should customize the wiki by overwriting templates, but soon learned that the only customization that really took place was that people forked the entire project. We don't want that for django-wiki, we want it to be modular and extendable.

As of now, Django has existed for too long without a proper wiki application. The dream of django-wiki is to become a contestant alongside Mediawiki, so that Django developers can stick to the Django platform even when facing tough challenges such as implementing a wiki.

Contributing
------------

This project will be very open for enrolling anyone with a good idea. As of now, however, it's a bit closed while we get the foundation laid out.

Q&A
------------

 * **Why is the module named just "wiki"?** Because "pip install wiki" returns "No distributions at all found for wiki"! :)
 * **What markup language will you use?** [Markdown](http://pypi.python.org/pypi/Markdown). The markup renderer is not a pluggable part but has been internalized into core parts. Discussion should go here: https://github.com/benjaoming/django-wiki/issues/76
 * **Why not use django-reversion?** It's a great project, but if the wiki has to grow ambitious, someone will have to optimize its behavior, and using a third-party application for something as crucial as the revision system is a no-go in this regard.
 * **Any support for multiple wikis?** Yes, in an sense you can just imagine that you always have multiple wikis, because you always have hierarchies and full control of their permissions. See this discussion: https://github.com/benjaoming/django-wiki/issues/63

Requirements
------------

So far the dependencies/requirements are:

 * [django>=1.5<1.7](http://www.djangoproject.com) - Django 1.7 will be released in version 0.1, but should run on 0.0.24
 * [django-south](http://south.aeracode.org/)
 * [Markdown>=2.2.0](https://github.com/waylan/Python-Markdown)
 * [django-mptt](https://github.com/django-mptt/django-mptt)
 * [django-sekizai](https://github.com/ojii/django-sekizai/)
 * [sorl-thumbnail](https://github.com/sorl/sorl-thumbnail)
 * Pillow (Python Imaging Library)
 * Python>=2.6 or Python>=3.2

Development
------------

The folder **testproject/** contains a pre-configured django project and an sqlite database. Login for django admin is *admin:admin*. This project should always be maintained, but please do not commit changes to the SQLite database as we only care about its contents in case data models are changed.


Acknowledgements
----------------

 * The people at [edX](http://www.edxonline.org/) & MIT for finding and supporting the project both financially and with ideas.
 * [django-cms](https://github.com/divio/django-cms) for venturing where no django app has gone before in terms of well-planned features and high standards. It's a very big inspiration.
 * [django-mptt](https://github.com/django-mptt/django-mptt), a wonderful utility for inexpensively using tree structures in Django with a relational database backend.
 * [spookylukey](https://github.com/spookylukey), [jluttine](https://github.com/jluttine), [cXhristian](https://github.com/cXhristian), [valberg](https://github.com/valberg), [jdcaballerov](https://github.com/jdcaballerov), [yekibud](https://github.com/yekibud), [bridger](https://github.com/bridger), [TomLottermann](https://github.com/TomLottermann), [crazyzubr](https://github.com/crazyzubr), and [everyone else](https://github.com/benjaoming/django-wiki/contributors) involved!

<!---Illegal PyPi RST data -->
<!---Anything that isn't validly translateable to PyPi RST goes after this line -->

Badgers Badgers Badgers
-----------------------

[![Docs](https://readthedocs.org/projects/django-wiki/badge/?version=latest)](http://django-wiki.readthedocs.org/)

[![Build Status](https://travis-ci.org/django-wiki/django-wiki.png?branch=master)](https://travis-ci.org/django-wiki/django-wiki)

[![Coverage Status](https://coveralls.io/repos/django-wiki/django-wiki/badge.svg?branch=master)](https://coveralls.io/r/django-wiki/django-wiki?branch=master)

[![Downloads](https://pypip.in/d/wiki/badge.png)](https://crate.io/package/wiki)

[![Downloads](https://pypip.in/v/wiki/badge.png)](https://crate.io/package/wiki)

[![Documentation Status](https://readthedocs.org/projects/django-wiki/badge/?version=latest)](https://readthedocs.org/projects/django-wiki/?badge=latest)

[![Dependency Status](https://gemnasium.com/django-wiki/django-wiki.svg)](https://gemnasium.com/django-wiki/django-wiki)
