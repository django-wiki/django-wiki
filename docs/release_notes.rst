Release notes
=============


About the versioning
--------------------

Up until the django-wiki 0.1 release, versions have been 0.0.1-0.0.24 with
migrations kept in South and without any serious issues of upgrading,
``python manage.py migrate`` was enough.

*django-wiki 0.1* is cutting ties in the sense that migrations are being reset.
This means that you can upgrade directly the upcoming 0.0.24 to 0.1 but upgrades
from previous versions are not possible.


django-wiki 0.0.24
------------------

This release is a transitional release for anyone still using an older version
of django-wiki. The code base has been heavily refactored and this is hopefully
the final release.

.. warning::
   0.0.24 is actually mainly a transitional release.

**Compatibility**

 * Django 1.5, 1.6 (That means Django 1.7 is **not** yet fully supported)
 * South 1.0+ (if you are on an older South, you **need** to upgrade)
 * Python 2.6, 2.7, 3.3, 3.4

**Notifications fixed**

Through its history, django-wiki has maintained `a very weird migration`_. It
caused for the notifications plugin's table to be removed, but luckily that
makes it quite easy to detect and restore, which the new migrations now do.

.. _ https://github.com/django-wiki/django-wiki/commit/88847096354121c23d8f10463201da5e0ebd7148

However, you may want to bootstrap having notifications. You can ensure that
all owners and editors of articles receive notifications using the following
management command:

    python manage.py wiki_notifications_create_defaults


Troubleshooting
___________________


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

django-wiki 0.1
---------------

.. warning::
   If you are upgrading from a previous release, please ensure that you
   firstly install django-wiki 0.0.24 because it contains the final migrations
   necessary before entering the django-wiki 0.1+ migration tree.
   
   If you are using django 1.7 and have an old installation of django-wiki
   (which should be impossible since it wouldn't run) please downgrade to 1.6,
   
   ::
   
       $ pip install django-wiki==0.0.24
       $ python manage.py migrate
       $ # EDIT YOUR PROJECT'S SETTINGS
       $ pip install django-wiki==0.3
       $ python manage.py migrate
   
   *Ammending settings*: If you are running django < 1.7, you need the following
   in your project's settings:
   
   ::
   
      INSTALLED_APPS.append('south')


**Supported**

 * Python 2.7, 3.3, and 3.4 (3.2 is not)
 * Django 1.5, 1.6 and 1.7
 * Django < 1.7 still needs south, and migration trees are kept until next major
   release.
   
Release plan:

Until django-wiki 0.2 is released, table names of plugins will defer depending
on whether you are using South or django.db.migrations. If you want to upgrade
your django to 1.7, please rename tables manually.

Django-wiki 0.2 will *not* support South.. but development will remain in the
0.1 branch for now.

New features are introduced in the 0.1 branch until something seriously has to
break due to some force majeure.
