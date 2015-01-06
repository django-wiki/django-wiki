Release notes
=============

.. warning::
   THIS IS A DRAFT, NONE OF THE BELOW ARE RELEASED YET!!


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

 * Django < 1.7 (That means Django 1.7 is **not** supported)
 * South 0.8.4+ (if you are on an older South, you **need** to upgrade)

**Notifications**

After upgrading, your first migrate will give the following error:

::

     ! These migrations are in the database but not on disk:
        <notifications: 0002_auto__del_articlesubscription>
     ! I'm not trusting myself; either fix this yourself by fiddling
     ! with the south_migrationhistory table, or pass --delete-ghost-migrations
     ! to South to have it delete ALL of these records (this may not be good).


If you are fine about loosing all subscriptions and recreate default
subscriptions after, just follow these steps:

::

    python manage.py migrate notifications zero --fake
    python manage.py migrate notifications
    python manage.py wiki_notifications_create_defaults


Further explanation
___________________

Unfortunately, previous releases of django-wiki have had the wrong APP_LABEL
set for wiki.plugins.notifications and thus all notification subscriptions
will be reset. The error could not be fixed as it was introduced in 0.0.23
as a stupid renaming of the notifications plugin tables with a subsequent
automatic removal of the original notifications tables.

So it's not actually a missing data migration in 0.0.24 that's the reason
why django-nyt starts out with zero subscriptions. It was a table renaming
in 0.0.23 that caused the error.

If you wish to preserve your subscription data as much as possible, you should
do a plain text dump of the table ``notifications_articlesubscription`` using
your database tools. At the end up the upgrade process, you will have to
manually import this data into the database.

If you are having problems, you need to re-run the migrations entirely.

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

In order to create notifications for all article authors and editors,
run the following management command:

::

    python manage.py wiki_notifications_create_defaults


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
      SOUTH_MIGRATION_MODULES = {
          'django_nyt': 'django_nyt.south_migrations',
          'wiki': 'wiki.south_migrations',
          'images': 'wiki.plugins.images.south_migrations',
          'notifications': 'wiki.plugins.notifications.south_migrations',
          'attachments': 'wiki.plugins.attachments.south_migrations',
      }
   


**Supported**

 * Python 2.7, 3.3, and 3.4 (3.2 is untested)
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
