Release notes
=============

About the versioning
--------------------

Up until the django-wiki 0.1 release, versions have been 0.0.1-0.0.24 with
migrations kept in South and without any serious issues of upgrading,
``python manage.py migrate`` was enough.

*django-wiki 0.1* is cutting ties in the sense that a project's


django-wiki 0.0.24
------------------

This release is a transitional release for anyone still using an older version
of django-wiki. The code base has been heavily refactored and this is hopefully
the final release.

.. warning::
   0.0.24 is actually mainly a transitional release.

**Compatibility**

 * Django < 1.7 (That means Django 1.7 is **not** supported)
 * South 0.8.4+ (if you are un an older South, you **need** to upgrade)

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
