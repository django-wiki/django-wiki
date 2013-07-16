Haystack plugin
===============

***July 16 2013***
Tested backend, xapian with Haystack 2.0. NB! Get the xapian from Git

https://github.com/notanumber/xapian-haystack

Not working
-----------

Do not use Whoosh, it has broken SearchQuerySet support and therefore will leak
articles that are set non-public.
