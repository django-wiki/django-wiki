Setting up a development environment
====================================

* Fork and clone the django-wiki repo from Github, ``cd`` into it.
* Create and activate a virtualenv for developing django-wiki.
  Ensure you are using recent setuptools and pip.
* Install the requirements::

    $ pip install --upgrade pip setuptools
    $ pip install -e .[devel]
    $ pip install tox
