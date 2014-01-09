django-wiki
===========

News
----

***News: November 18th, 2013***

Better late than never! A new release is out with promising support of django 1.6 and Bootstrap 3. Also, jquery, colorbox, and markitup editor have been bumped to newer releases.

A big callout to anyone who feels like getting into documentation.. we need good docs!

Also, the [Changelog](https://github.com/benjaoming/django-wiki/blob/master/CHANGELOG.md) is updated!

***News: June 31st, 2013***

**Bootstrap 3** has landed in the django-wiki master branch! However, a new release is pending the full implementation of Bootstrap 3. If you are running a deployment with template overrides, keep in mind that some Bootstrap stuff has changed, especially fluid grids and names of a lot of classes. For instance, if you have put your own "brand" in the navbar, you need to change `class="brand"` to `class="navbar-brand"`.

Furthermore, we have changed the **icon theme** to use Font Awesome. There are now many more icons to choose from, and most of the UI is likely to benefit from this.

The **plugin API** has been looking very stable lately, and [one](https://github.com/benjaoming/django-wiki/commit/c259b318b1c7bc74568d0c9000c016976b05d171) or [two](https://github.com/benjaoming/django-wiki/commit/384fb62040dbf27805352d83443467ce175c34c8) refactorings made it possible to much easier deal with circular dependencies which were greatly reducing the plugin writing experience.

**Haystack** is now supported through a plugin. But keep in mind that many things are broken in Haystack atm -- the Whoosh backend for instance.

Last, but not least, we have an **IRC channel** - #django-wiki on freenode. Please hangout and share support and tips!

***News: June 7th, 2013***

Yay! New alpha release! [View commit log on Github >](https://github.com/benjaoming/django-wiki/commits/alpha/0.0.20) or [a summary of all the commits](https://groups.google.com/forum/#!topic/django-wiki/ZnnGowlppj4)

Highlights:

- Fix missing translation activation in django-notify's email notifications (manage command) - credits TomLottermann
- Add Russian on django-wiki and django-notify - credits crazyzubr
- Support for AUTH_USER_MODEL settings (seriously, don't use it though, unless you really want trouble in most third party django apps). **Please note** this is only going to help you if you are starting new projects. If you are changing the setting and introducing a new model in a running project, you have to do all database migrations manually. Django-wiki and its South migrations will silently ignore your changes.
- Add settings for logging to files instead of stdout in django-notify daemon mode - credits: crazyzubr
- Built-in account handling now properly asserts that usernames are not already taken when signing up.

***News: April 23rd, 2013***

Security fix included in 0.0.19. [View commit log >](https://github.com/benjaoming/django-wiki/commits/alpha/0.0.19)

***News: March 26, 2013***

Thanks to TomLottermann for German translation and daltonmatos for Brazilian translations! French is also reported in the works. 0.0.18 is released with that plus Django 1.5 compatibility, and [a bunch of other things and fixes](https://groups.google.com/forum/#!topic/django-wiki/V-bZou8aTaI).

***News: February 21, 2013***

New release adds email notifications to django_notify, improved [toc] tag and bootstrap typography.

***News: February 8, 2013***

New alpha release 0.0.15 is out mainly because static files and templates in the previous two builds were not being properly updated and included. It also includes various tiny cosmetic changes and a new LESS structure.

(old news are deleted)

Demo
----

A demo is available here, sign up for an account to see the notification system.

[wiki.overtag.dk](http://wiki.overtag.dk)

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

Dependencies
------------

So far the dependencies are:

 * [django>=1.4](http://www.djangoproject.com)
 * [django-south](http://south.aeracode.org/)
 * [Markdown>=2.2.0](https://github.com/waylan/Python-Markdown)
 * [django-mptt>=0.5.3](https://github.com/django-mptt/django-mptt)
 * [django-sekizai](https://github.com/ojii/django-sekizai/)
 * [sorl-thumbnail](https://github.com/sorl/sorl-thumbnail)
 * Pillow (Python Imaging Library)
 * Python>=2.5<3 (Python 3 not yet supported)

Development
------------

In your Git fork, run `pip install -r requirements.txt` to install the requirements.

The folder **testproject/** contains a pre-configured django project and an sqlite database. Login for django admin is *admin:admin*. This project should always be maintained, but please do not commit changes to the SQLite database as we only care about its contents in case data models are changed.

[![Build Status](https://travis-ci.org/benjaoming/django-wiki.png?branch=master)](https://travis-ci.org/benjaoming/django-wiki)

[![Downloads](https://pypip.in/d/wiki/badge.png)](https://crate.io/package/wiki)

[![Downloads](https://pypip.in/v/wiki/badge.png)](https://crate.io/package/wiki)


Python 2.5
----------

It's compatible and being run on a server with Python 2.5.

Due to Markdown using elementree, you should check that you have python-celementtree: `apt-get install python-celementtree`

Acknowledgements
----------------

 * The people at [edX](http://www.edxonline.org/) & MIT for finding and supporting the project both financially and with ideas.
 * [django-cms](https://github.com/divio/django-cms) for venturing where no django app has gone before in terms of well-planned features and high standards. It's a very big inspiration.
 * [django-mptt](https://github.com/django-mptt/django-mptt), a wonderful utility for inexpensively using tree structures in Django with a relational database backend.
 * [jdcaballero](https://github.com/jdcaballero), [yekibud](https://github.com/yekibud), [bridger](https://github.com/bridger), [TomLottermann](https://github.com/TomLottermann), [crazyzubr](https://github.com/crazyzubr), and [everyone else](https://github.com/benjaoming/django-wiki/contributors) involved!

<!---Illegal PyPi RST data -->
<!---Anything that isn't validly translateable to PyPi RST goes after this line -->

