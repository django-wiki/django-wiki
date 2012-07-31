django-wiki
===========

*2012-07-27*

!THIS IS A WORK IN PROGRESS
---------------------------

This is where it all begins. In less than 4 weeks we should have a wiki system appealing to any kind of Django developer out there. Here is the manifest (so far):

 * **Be pluggable and light-weight.** Don't integrate optional features in the core.
 * **Be open.** Make an extension API that allows the ecology of the wiki to grow. After all, Wikipedia consists of some [680 extensions](http://svn.wikimedia.org/viewvc/mediawiki/trunk/extensions/) written for MediaWiki.
 * **Be smart.** [This is](https://upload.wikimedia.org/wikipedia/commons/8/88/MediaWiki_database_schema_1-19_%28r102798%29.png) the map of tables in MediaWiki - we'll understand the choices of other wiki projects and make our own. After-all, this is a Django project.
 * **Be simple.** The source code should explain itself.
 * **Be structured.** Markdown is a simple syntax for readability. Features should be implemented either through easy coding patterns in the content field, but rather stored in a structured way (in the database) and managed through a friendly interface. This gives control back to the website developer, and makes knowledge more usable. Just ask: Why has Wikipedia never changed? Answer: Because it's knowledge is stored in a complicated way, thus it becomes very static.

Installation
------------

    pip install git+git://github.com/benjaoming/django-wiki.git

After that, add `'wiki'` to `settings.INSTALLED_APPS`.

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
 * **What markup language will you use?** The markup engine will be pluggable, but Markdown will be the built-in supported one.
 * **Why not use django-reversion?** It's a great project, but if the wiki has to grow ambitious, someone will have to optimize its behavior, and using a third-party application for something as crucial as the revision system is a no-go in this regard.

Dependencies
------------

So far the dependencies are:

 * [django=>1.4](http://www.djangoproject.com)
 * [django-south](http://south.aeracode.org/)
 * [Markdown>=2.2.0](https://github.com/waylan/Python-Markdown)
 * [django-mptt>=0.5](https://github.com/django-mptt/django-mptt)
 * [django-sekizai](https://github.com/ojii/django-sekizai/)

Acknowledgements
----------------

 * The people at [edX](http://www.edxonline.org/) & MIT for finding and supporting the project both financially and with ideas.
 * [django-cms](https://github.com/divio/django-cms) for venturing where no django app has gone before in terms of well-planned features and high standards. It's a very big inspiration.

