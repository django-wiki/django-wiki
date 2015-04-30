Known Issues
============

Django 1.4
----------

1.4.2+

* In the requirements is stated ``sorl-thumbnail>11.12.1b`` which is the newest beta of sorl-thumbnail. However, you need to downgrade after.
* [django-mptt issue #271](https://github.com/django-mptt/django-mptt/issues/271) means that you should use Django 1.4.2+.

Django 1.7+ and Python 2.6
--------------------------

Those are incompatible with each other and can never be combined as Dj 1.7 dropped Py 2.6 support.
