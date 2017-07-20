Release notes
=============


Release plan
------------

The next release series **0.3** will support Django 1.11. Likewise, it will be
the last series with Python 2 support. Series 0.3 is in development in the
current master branch and the latest pre-release is available with
`pip install wiki --pre`.


django-wiki 0.3b1
-----------------

 * Test refactor: Use django-functest and separate WebTest from Selenium (Luke Plant) #634
 * Django 1.11 compatibility (Luke Plant) #634
 * Repo refactor: Moved ``wiki`` package to ``src/`` folder and test code to ``tests/`` #631
 * New bootstrapped image insert dialog (Frank Loemker) #628
 * Allow the HTML tag ``<hr>`` (Frank Loemker) #629
 * Global History overview of page revisions (Frank Loemker and Maximilien Cuony) #627
 * Move article support with redirects (Frank Loemker) #640
 * Crop paginator window when there are >9 pages in a list (Frank Loemker) #646
 * Render django.contrib.messages with template tag and inclusion template: Configurable and bootstrap 3 compatible (Benjamin Bach and Frank Loemker) #654
 * Don't hardcode redirect url in account update view (Benjamin Bach) #650
 * Python 3.6 support added to test matrix (Benjamin Bach) #664


django-wiki 0.2.4
-----------------

 * Hot-fix because of missing woff2 files #625


django-wiki 0.2.3
-----------------

 * Pulled Transifex translations and pushed source translations.
 * Fix support for Py2 unicode in code blocks (Benjamin Bach) #607
 * Support for Github style fenced codeblocks (Benjamin Bach) #618
 * Cached articles showing up in wrong language (Benjamin Bach) #592
 * Upgraded Bootstrap from 3.3.1 to 3.3.7 (Benjamin Bach) #620
 * Upgraded bundled jQuery to 1.12.4 (Benjamin Bach) #620
 * Setting ``WIKI_MARKDOWN_HTML_STYLES`` for allowing ``style='..'`` in user code (Benjamin Bach) #603
 * Strip Markdown code in search result snippets (Benjamin Bach) #42


django-wiki 0.2.2
-----------------

 * Remove ``wiki.decorators.json_view``, fixes server errors when resolving 404 links #604
 * Replace usage of ``render_to_response()`` with ``render()`` #606
 * Fix memory leak #609 and #611 (obtroston)
 * Scroll bars and display area fixed for code blocks #601 and #608 (Branko Majic)
 * Option ``WIKI_MARKDOWN_SANITIZE_HTML`` skips Bleach (warning: Don't use for untrusted code) #610 (Michal Hozza)
 * Allow the HTML tag ``<br>``. #613 (Frank Loemker)
 * Add thumbnail size directive (example: ``[image:123 size:large]``). #612 (Frank Loemker and @inflrscns)
 * Fix error with absolute paths in wiki links (example: ``[Sub-root](wiki:/sub-root)``) #616 (Benoit C. Sirois)
 * Require ``Django<1.11`` #616 (Benoit C. Sirois)


django-wiki 0.2.1
-----------------

 * Lowercase slugs when creating new pages with ``[[Like This]]`` #595 (Eric Clack)
 * Fix issues related to Bleach before Markdown processing esp. pertaining ``>`` characters. #596
 * Remove ``wiki.plugins.mediawikiimport`` #597
 * Pretty up the highligted code's line enumeration #598
 * Customize codehilite in order to wrap highlighted code with scrollbars #598


django-wiki 0.2
---------------

 * Translation updates from Transifex

   * Danish translation from 39% to 100% (Bo Holm-Rasmussen)
   * Updated languages since 0.1: Chinese, French, German, German, Russian, Spanish

 * Added Django 1.10 support #563
 * Security: Do not depend on markdown ``safe_mode``, instead use ``bleach``.
 * Fix duplicate search results when logged in #582 (duvholt)
 * Do not allow slugs only consisting of numbers #558
 * Copy in urlify.js and fix auto-population of slug field in Django 1.9+ #554
 * Fix memory leak in markdown extensions setting #564
 * Updated translations - Languages > 90% completed: Chinese (China), Portuguese (Brazil), Korean (Korea), French, Slovak, Spanish, Dutch, German, Russian, Finnish.
 * Taiwanese Chinese added (39% completed)
 * Cleanup documentation structure #575

HTML contents
~~~~~~~~~~~~~

`Bleach <https://github.com/mozilla/bleach>`_ is now used to sanitize HTML
before invoking Markdown.

HTML escaping is done before Markdown parsing happens. In future Markdown
versions, HTML escaping is no longer done, and ``safe_mode`` is removed. We have
already removed ``safe_mode`` from the default ``WIKI_MARKDOWN_KWARGS`` setting,
however if you have configured this yourself, you are advised to remove
``safe_mode``.

Allowed tags are from Bleach's default settings: ``a``, ``abbr``, ``acronym``,
``b``, ``blockquote``, ``code``, ``em``, ``i``, ``li``, ``ol``, ``strong``,
``ul``.

Please use new setting ``WIKI_MARKDOWN_HTML_WHITELIST`` and set a list of
allowed tags to customize behavior.


Python and Django support
~~~~~~~~~~~~~~~~~~~~~~~~~

Support has been removed for:

 * Python 2.6
 * Django < 1.8
 * South

django-wiki 0.1.2
-----------------

 * Remove unwanted items from default menu when ``WIKI_ACCOUNT_HANDLING = False``. #545
 * Fix broken soft-deletion and restoring of images, and "set revision" functionality #533
 * Added responsiveness to tables by use of Bootstrap table-responsive class #552


django-wiki 0.1.1
-----------------

 * Several languages updated from Transifex

   * Slovak added **Thanks M Hozza**
   * Portuguese also added, but as copy of PT-BR (make changes as desired in Transifex)

 * Brand new Account Settings page (email / password) **Thanks inflrscns**
 * Testproject turned into Django 1.9 layout
 * Replace context-processor dependent use of ``{{ STATIC_URL }}`` with ``{% static %}``
 * Bugfix for ``pip install wiki`` in an empty (no Django installed) virtualenv
 * Precommit hooks added in repository
 * Import statements sorted and codebase re-pep8'thed
 * Log in page is now called "Log in" in ``<title>`` tag - **Thanks Eugene Obukhov**


django-wiki 0.1
---------------

.. warning::
   If you are upgrading from a previous release, please ensure that you
   pass through the 0.0.24 release because it contains the final migrations
   necessary before entering the django-wiki 0.1+ migration tree.
   
   If you are using django 1.7+ and have an old installation of django-wiki
   (which should be impossible since it wouldn't run) please downgrade to 1.6
   as follows:
   
   ::
   
       $ pip install wiki\<0.1 --upgrade  # Latest 0.0.24 release
       $ pip install django\<1.7  # Downgrade django if necessary
       $ python manage.py migrate  # Run 0.0.24 migrations
       $ pip install wiki\<0.2 --upgrade  # Upgrade to latest 0.1 series
       $ python manage.py migrate --delete-ghost-migrations  # Run migrations again,
                                                             # removing the (ghost) 
                                                             # migrations from previous
                                                             # release
       $ # Feel free to upgrade Django again


**Supported**

 * Python 2.7, 3.3, 3.4, 3.5 (3.2 is not supported)
 * Django 1.5, 1.6, 1.7, 1.8, 1.9
 * Django < 1.7 still needs South, and migration trees are kept until next major
   release.


Breaking changes
~~~~~~~~~~~~~~~~

**wiki.VERSION as tuple**

We want to follow Django's way of enumerating versions. If you want the old
string version, use ``wiki.__version__``.

**Plugin API**

Since Django 1.8 has started making warnings about `patterns` being deprecated, we've decided
to stop using them by default. Thus, as with the future Django 2.0, we will use lists of `url`
objects to store the urlconf of plugins. All the bundled plugins have been updated to reflect
the change.

**Django-mptt**

We now depend on django-mptt 0.7.2+ for Django 1.8 compatibility.


django-wiki 0.0.24
------------------

This release is a transitional release for anyone still using an older version
of django-wiki. The code base has been heavily refactored and this is hopefully
the final release.

.. warning::
   0.0.24 is mainly a transitional release, but new features and bug fixes are
   included, too.

**Compatibility**

 * Django 1.5, 1.6 (That means Django 1.7 is **not** yet fully supported)
 * South 1.0+ (if you are on an older South, you **need** to upgrade)
 * Python 2.6, 2.7, 3.3, 3.4


Upgrading
~~~~~~~~~

Firstly, upgrade django-wiki through familiar steps with pip

::

    $ pip install wiki --upgrade
   
During the upgrade, notice that `django-nyt`_ is installed. This replaces the
previously bundled django_notify and you need to make a few changes in
your settings and urls.

.. _django-nyt: https://github.com/benjaoming/django-nyt

In ``settings.INSTALLED_APPS``, replace `"django_notify"` with `"django_nyt"`.
Then open up your project's urlconf and make sure you have something
that looks like the following:

::

    from wiki.urls import get_pattern as get_wiki_pattern
    from django_nyt.urls import get_pattern as get_nyt_pattern
    urlpatterns += patterns('',
        (r'^notifications/', get_nyt_pattern()),
        (r'', get_wiki_pattern())
    )

Notice that we are importing `from django_nyt.urls` and no longer
`django_notify` and that the function is renamed to `get_nyt_pattern`.

After making these changes, you should run migrations.

::

    $ python manage.py migrate


**Notifications fixed**

In past history, django-wiki has shipped with `a very weird migration`_. It
caused for the notifications plugin's table of article subscriptions to be removed.
This is fixed in the new migrations and the table should be `safely restored`_ in
case it was missing.

.. _a very weird migration: https://github.com/django-wiki/django-wiki/commit/88847096354121c23d8f10463201da5e0ebd7148
.. _safely restored: https://github.com/django-wiki/django-wiki/blob/releases/0.0.24/wiki/plugins/notifications/south_migrations/0003_conditionally_restore_articlesubscription.py

However, you may want to bootstrap subscription notifications in case you have run
into this failed migration. You can ensure that all owners and editors of articles
receive notifications using the following management command:

    python manage.py wiki_notifications_create_defaults


Troubleshooting
~~~~~~~~~~~~~~~


If you have been running from the git master branch, you may experience
problems and need to re-run the migrations entirely.

::

    python manage.py migrate notifications zero --delete-ghost-migrations
    python manage.py migrate notifications

If you get `DatabaseError: no such table: notifications_articlesubscription`,
you have been running django-wiki version with differently named tables.
Don't worry, just fake the backwards migration:

::

    python manage.py migrate notifications zero --fake  

If you get ``relation "notifications_articlesubscription" already exists`` you
may need to do a manual ``DROP TABLE notifications_articlesubscription;`` using
your DB shell (after backing up this data).

After this, you can recreate your notifications with the former section's
instructions.



News archive
------------

April 15, 2017
~~~~~~~~~~~~~~

0.2.3 released: `Release notes <http://django-wiki.readthedocs.io/en/master/release_notes.html#django-wiki-0-2-3>`_

0.2.2 released: `Release notes <http://django-wiki.readthedocs.io/en/master/release_notes.html#django-wiki-0-2-2>`_


February 27, 2017
~~~~~~~~~~~~~~~~~

0.2.1 released: `Release notes <http://django-wiki.readthedocs.io/en/master/release_notes.html#django-wiki-0-2-1>`_


December 27, 2016
~~~~~~~~~~~~~~~~~

0.2 final released: `Release notes <http://django-wiki.readthedocs.io/en/0.2/release_notes.html>`_


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

