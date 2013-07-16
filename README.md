django-wiki
===========

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

Use our mailing list (google group) for getting in touch on development and support:

[django-wiki@googlegroups.com](https://groups.google.com/d/forum/django-wiki)

[twitter:djangowiki](https://twitter.com/djangowiki)

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

Installation
------------

### Pre-requisites

Django-wiki uses the [PIL library](http://www.pythonware.com/products/pil/) for image processing. The preferred method should be to get a system-wide version of PIL, for instance by getting the binaries from your Linux distribution repos.

**PIL Directly from repository: Debian-based Linux Distros**

    sudo apt-get install python-imaging

**PIL/Pillow for Pypi**

Firstly, you need to get development libraries that PIP needs before compiling. For instance on Debian/Ubuntu:

    sudo apt-get install libjpeg8 libjpeg-dev libpng libpng-dev

After that, choose either `pip install PIL` or `pip install Pillow`. Pillow is the pip-friendly version of PIL. You might as well install PIL system-wide, because there are little version-specific dependencies in Django applications when it comes to PIL.

**Mac OS X 10.5+**

[Ethan Tira-Thompson](http://ethan.tira-thompson.com/Mac_OS_X_Ports.html) has created ports for OS X and made them available as a .dmg installer.  Download and install the universal combo package [here](http://ethan.tira-thompson.com/Mac_OS_X_Ports_files/libjpeg-libpng%20%28universal%29.dmg).

Once you have the packages installed, you can proceed to the pip installation.  PIL will automatically pick up these libraries and compile them for django use.

### Install
To install the latest stable release:

`pip install wiki`

Install directly from Github, since there is no release yet:

`pip install git+git://github.com/benjaoming/django-wiki.git`

### Configure `settings.INSTALLED_APPS`

The following applications should be listed - NB! it's important to maintain the order due to database relational constraints:
    
        'django.contrib.humanize',
        'south',
        'django_notify',
        'mptt',
        'sekizai',
        'sorl.thumbnail',
        'wiki',
        'wiki.plugins.attachments',
        'wiki.plugins.notifications',
        'wiki.plugins.images',
        'wiki.plugins.macros',

### Database

To sync and create tables, do:

    python manage.py syncdb
    python manage.py migrate

### Configure TEMPLATE_CONTEXT_PROCESSORS

Add `'sekizai.context_processors.sekizai'` and `'django.core.context_processors.debug'` to `settings.TEMPLATE_CONTEXT_PROCESSORS`. Please refer to the [Django docs](https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors) to see the current default setting for this variable.

In Django 1.5, it should look like this:

    TEMPLATE_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.request",
        "django.core.context_processors.static",
        "django.core.context_processors.tz",
        "django.contrib.messages.context_processors.messages",
        "sekizai.context_processors.sekizai",
    )

### Include urlpatterns

To integrate the wiki to your existing application, you shoud add the following lines at the end of your project's `urls.py`.

    from wiki.urls import get_pattern as get_wiki_pattern
    from django_notify.urls import get_pattern as get_notify_pattern
    urlpatterns += patterns('',
        (r'^notify/', get_notify_pattern()),
        (r'', get_wiki_pattern())
    )

Please use these function calls rather than writing your own include() call - the url namespaces aren't supposed to be customized.

The above line puts the wiki in */* so it's important to put it at the end of your urlconf. You can also put it in */wiki* by putting `'^wiki/'` as the pattern.

### Settings

For now, look in [wiki/conf/settings.py](https://github.com/benjaoming/django-wiki/blob/master/wiki/conf/settings.py) to see a list of available settings.

### Other tips

 1. **Account handling:** There are simple views that handle login, logout and signup. They are on by default. Make sure to set settings.LOGIN_URL to point to your login page as many wiki views may redirect to a login page.

Plugins
------------

Add/remove the following to your `settings.INSTALLED_APPS` to enable/disable the core plugins:

 * `'wiki.plugins.attachments'`
 * `'wiki.plugins.images'`
 * `'wiki.plugins.notifications'`

The notifications plugin is mandatory for an out-of-the-box installation. You can safely remove it from INSTALLED_APPS if you also override the **wiki/base.html** template.

Any docs?
---------

**No**, but there is a `docs/` skeleton and a RTD project has been registered. If you wish to write something, you can start with contents from this page, and please ask in the google group or raise an issue if you're in doubt about whether something might change.

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
 * PIL (Python Imaging Library)
 * Python>=2.5<3 (Python 3 not yet supported)

Development
------------

In your Git fork, run `pip install -r requirements.txt` to install the requirements.

The folder **testproject/** contains a pre-configured django project and an sqlite database. Login for django admin is *admin:admin*. This project should always be maintained, but please do not commit changes to the SQLite database as we only care about its contents in case data models are changed.

[![Build Status](https://travis-ci.org/benjaoming/django-wiki.png?branch=master)](https://travis-ci.org/benjaoming/django-wiki)

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

Support
-------

This project is already alive and will remain alive, because it's free software and as long as it's essential, common interest will keep it alive... we hope :) You're more than welcome to show your appreciation through Flattr.

[![Flattr this git repo](http://api.flattr.com/button/flattr-badge-large.png)](https://flattr.com/submit/auto?user_id=benjaoming&url=https://github.com/benjaoming/django-wiki/&title=django-wiki&language=&tags=github&category=software) 
