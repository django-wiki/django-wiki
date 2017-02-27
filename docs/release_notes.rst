Release notes
=============


Release plan
------------

Currently, the only series in development is the 0.2 series, and all bug fixes
and new features are referred to this series, keeping in mind that they don't
introduce any backwards incompatible changes.

django-wiki 0.2.2 (unreleased master branch)
--------------------------------------------

 * Changes go here


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
________________

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
_________

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
_______________


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


