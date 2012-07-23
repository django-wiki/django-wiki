django-wiki
===========

This is where it all begins. In 4 weeks we should have a wiki system appealing to any kind of Django developer out there. Here is the manifest (so far):

 * Be pluggable and light-weight. Don't integrate optional features in the core.
 * Be open. Make an extension API that allows the ecology of the wiki to grow. Afterall, Wikipedia consists of some [680 extentions](http://svn.wikimedia.org/viewvc/mediawiki/trunk/extensions/) written for MediaWiki.
 * Be smart. [This is](https://upload.wikimedia.org/wikipedia/commons/8/88/MediaWiki_database_schema_1-19_%28r102798%29.png) the map of tables in MediaWiki. We don't want that.
 * Be simple. The source code should explain itself.

Background
----------

Django-wiki is a rewrite of [django-simplewiki](http://code.google.com/p/django-simple-wiki/), a project from 2009 that aimed to be a base system for a wiki. It proposed that the user should customize the wiki by overwriting templates, but soon learned that the only customization that people did was by forking the whole project. We don't want that.

Contributing
------------

This project will be very open for enrolling anyone with a good idea. As of now, however, it's a bit closed while we get the foundation laid out.

Q&A
------------

 * '''Why is the module named just "wiki"?''' Because "pip install wiki" returns "No distributions at all found for wiki"! :)
 * '''What markup language will you use?''' The markup engine will be pluggable, but Markdown will be the builtin supported one.

