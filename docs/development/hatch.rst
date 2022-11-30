pyproject.toml and hatch
========================

Initially, django-wiki core devs opted to use the
new ``pyproject.toml`` and drop the old ``setup.py`` (see
:url-issue:`1199`). The Python packaging ecosystem has
standardized on the interface for build backends
(`PEP 517 <https://peps.python.org/pep-0517/>`_/`PEP 660 <https://peps.python.org/pep-0660/>`_)
and the format for metadata declaration (`PEP 621 <https://peps.python.org/pep-0621/>`_/`PEP 631 <https://peps.python.org/pep-0631/>`_).
As a result, the execution of ``setup.py`` files is now `deprecated <https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html>`_.

The discussion for this feature and the steps to mark this as completed are
happening `in this discussion <https://github.com/django-wiki/django-wiki/discussions/1226>`_,
and as well the development process is `here <https://github.com/django-wiki/django-wiki/pull/1227>`_.

As a result of this work, the maintainers opted to use ``hatch`` to manage the
development process of django-wiki, you can read more about it in their
`official docs <https://hatch.pypa.io/latest/>`_.

Assuming you have installed ``hatch`` in your environment, the first thing that
you have to do in a fresh copy of ``django-wiki`` is to initilize the
environments, for that you have to execute ``hatch env create`` in the root of
``django-wiki`` codebase.

This will add a set of available commands, and different environment that are
used in the development process, here's a list generated with ``hatch env show``::

                             Standalone
  +-----------+---------+---------------------------+-------------+
  | Name      | Type    | Dependencies              | Scripts     |
  +===========+=========+===========================+=============+
  | default   | virtual | black<22.11,>=22.3.0      | assets      |
  |           |         | codecov                   | clean-build |
  |           |         | coverage[toml]            | clean-pyc   |
  |           |         | ddt                       | cov         |
  |           |         | django-functest<1.6,>=1.2 | lint        |
  |           |         | flake8<5.1,>=3.7          | no-cov      |
  |           |         | pre-commit                | test        |
  |           |         | pytest-cov                |             |
  |           |         | pytest-django             |             |
  |           |         | pytest-pythonpath         |             |
  |           |         | pytest<7.3,>=6.2.5        |             |
  +-----------+---------+---------------------------+-------------+
  | transifex | virtual | transifex-client          | assets      |
  |           |         |                           | clean-build |
  |           |         |                           | clean-pyc   |
  |           |         |                           | cov         |
  |           |         |                           | lint        |
  |           |         |                           | no-cov      |
  |           |         |                           | pull        |
  |           |         |                           | push        |
  |           |         |                           | test        |
  +-----------+---------+---------------------------+-------------+
  | docs      | virtual | bleach<5.1,>=3.3.0        | assets      |
  |           |         | django>=3.1.13            | build       |
  |           |         | sphinx-rtd-theme==1.1.1   | changes     |
  |           |         | sphinx>=3                 | clean       |
  |           |         |                           | clean-build |
  |           |         |                           | clean-pyc   |
  |           |         |                           | cov         |
  |           |         |                           | devhelp     |
  |           |         |                           | dirhtml     |
  |           |         |                           | doctest     |
  |           |         |                           | epub        |
  |           |         |                           | gettext     |
  |           |         |                           | html        |
  |           |         |                           | htmlhelp    |
  |           |         |                           | info        |
  |           |         |                           | json        |
  |           |         |                           | latex       |
  |           |         |                           | latexpdf    |
  |           |         |                           | link-check  |
  |           |         |                           | link-check2 |
  |           |         |                           | lint        |
  |           |         |                           | man         |
  |           |         |                           | no-cov      |
  |           |         |                           | pickle      |
  |           |         |                           | qthelp      |
  |           |         |                           | singlehtml  |
  |           |         |                           | test        |
  |           |         |                           | texinfo     |
  |           |         |                           | text        |
  +-----------+---------+---------------------------+-------------+
                                      Matrices
  +------+---------+-------------------+---------------------------+-------------+
  | Name | Type    | Envs              | Dependencies              | Scripts     |
  +======+=========+===================+===========================+=============+
  | test | virtual | test.py3.7-dj2.2  | black<22.11,>=22.3.0      | all         |
  |      |         | test.py3.7-dj3.0  | codecov                   | assets      |
  |      |         | test.py3.7-dj3.1  | coverage[toml]            | clean       |
  |      |         | test.py3.7-dj3.2  | ddt                       | clean-build |
  |      |         | test.py3.8-dj2.2  | django-functest<1.6,>=1.2 | clean-pyc   |
  |      |         | test.py3.8-dj3.0  | flake8<5.1,>=3.7          | cov         |
  |      |         | test.py3.8-dj3.1  | pre-commit                | lint        |
  |      |         | test.py3.8-dj3.2  | pytest-cov                | no-cov      |
  |      |         | test.py3.9-dj2.2  | pytest-django             | test        |
  |      |         | test.py3.9-dj3.0  | pytest-pythonpath         |             |
  |      |         | test.py3.9-dj3.1  | pytest<7.3,>=6.2.5        |             |
  |      |         | test.py3.9-dj3.2  |                           |             |
  |      |         | test.py3.10-dj3.2 |                           |             |
  |      |         | test.py3.8-dj4.0  |                           |             |
  |      |         | test.py3.9-dj4.0  |                           |             |
  |      |         | test.py3.10-dj4.0 |                           |             |
  +------+---------+-------------------+---------------------------+-------------+


We have 4 different environments declared in the configuration file, each one
has his own purpose:

* ``default``: The development environment for django-wiki.

* ``test``: where we ensure that the code works on different Django and Python versions.

* ``docs``: Used for generate the page you're reading at this moment.

* ``transifex``: Used only for the translation side of the project.

We center around the entrypoints provided by ``hatch`` (`read more <https://hatch.pypa.io/latest/environment/#scripts>`_)
that's why we have documented commands that make development easier.
Some commands are only available in certain environments,
so for example at the ``transifex`` environment you see ``pull`` and ``push``
commands that are not present in any other environment declared above. For
executing the command you have to follow this simple formula::

  $ hatch run <environment name>:<command name>

Then applied to the ``push`` command on the ``transifex`` environment will be::

  $ hatch run transifex:pull

You can use the same logic to execute the available commands in the app, but
heres a detailed list of the commands ordered by environments, so you can
understand the purpose of each one:

* ``cov``: Check coverage status.

* ``no-cov``: Check places pending to add coverage.

* ``lint``: Make sure the code changes follow our guidelines and conventions.

* ``clean-build``: Remove the files generated after the project is built.

* ``clean-pyc``: Remove pyc generated files.

* ``assets``: Generate the static files used by django-wiki frontend.

* ``test``: Test the changes in the current environment.

* ``test:all``: Test the changes across our supported Python and Django versions.

* ``test:lint``: Make sure the code changes follows our guidelines and conventions.

* ``test:clean``: Remove the files generated via the testing process.

* ``transifex:push``: Push the translation files to Transifex.

* ``transifex:pull``: Pull the translation files from Transifex.

* ``docs:clean``: Remove the generated documentation files.

* List of docs commands used to generate the documentation in different formats:

  * Please refer to the `Builder documentation of SPHINX <https://www.sphinx-doc.org/en/master/usage/builders/index.html>`_
    to understand more about the purpose of each builder and the expected output.

  * ``docs:html``

  * ``docs:dirhtml``

  * ``docs:singlehtml``

  * ``docs:pickle``

  * ``docs:json``

  * ``docs:htmlhelp``

  * ``docs:qthelp``

  * ``docs:devhelp``

  * ``docs:epub``

  * ``docs:latex``

  * ``docs:latexpdf``

  * ``docs:text``

  * ``docs:man``

  * ``docs:texinfo``

  * ``docs:info``

  * ``docs:gettext``

  * ``docs:changes``

  * ``docs:link-check2``

  * ``docs:doctest``


* ``docs:build``: Generate the documentation in HTML format.

* ``docs:link-check``: Checks for external links across the documentation.

We hope that this document helps you to understand more about the development
process, if something is not clear please open an issue.

FAQ
---

1. **Whats the difference between test and test:all?**

   When you execute ``hatch run test`` this will check your changes in the
   active environment, this means it will run over an specific Python version
   and an specific Django Version; in the other hand ``test:all`` will run the
   test suite in the whole matrix of the supported versions of Python and Django.

2. **hatch is unable to create a test environment with an specific Python Version?**

   If after you execute ``hatch env create`` you receive a message like this in
   your terminal ``py3.8-4.0 -> cannot locate Python: 3.8`` this means that
   ``hatch`` was unable to locate that Python version, in the end it depends on
   what program do you use for manage your Python version, the most
   important part is that the versions must be available in your ``PATH``.

3. **How to manage different Python Versions?**

   There's a lot of options outside, the most important piece is that as stated
   above, the versions need to able to be located in your system ``PATH``. for
   example, if you're a user of `pyenv <https://github.com/pyenv/pyenv>`_ you
   can set multiple Python version using ``pyenv local <version> <version>``.

   ``pyenv local 3.7.12 3.8.12 3.9.13 3.10.2``

 4. **There's an error when init an environment?**

   If you see and error message like ``Environment default defines a matrix, choose one of the following instead:``
   and then a list of all of the available environments, you need to set the
   environment name on the shell command like this ``hatch -e <env_name> shell``

   ``hatch -e test.py3.10-dj3.2 shell``

   This way you can switch environments by an specific Python and Django version.

 5. **How do I switch default shell versions?**

    By default django-wiki runs on the latest supported Python and Django
    version, if you want to swich to another environment, say for example
    Python 3.9.13 with Django 3.0 then execute the following command:

    ``hatch -e py3.9-dj3.0 shell``
