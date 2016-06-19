Release notes
=============


About the versioning
--------------------

Up until the django-wiki 0.1 release, versions have been 0.0.1-0.0.24 with
migrations kept in South and without any serious issues of upgrading,
``python manage.py migrate`` was enough.

*django-wiki 0.1* is cutting ties and migrations are being reset.
This means that you can upgrade directly from upcoming 0.0.24 to 0.1 but upgrades
from previous versions bypassing 0.0.24 are not possible.


Release plan
------------

Until django-wiki 0.2 is released, table names of plugins will defer depending
on whether you are using South or django.db.migrations. If you want to upgrade
your django to 1.7, please rename tables manually.

Django-wiki 0.2 will *not* support South.. but development will remain in the
0.1 branch for now.

New features are introduced in the 0.1 branch until something seriously has to
break due to some force majeure.


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


