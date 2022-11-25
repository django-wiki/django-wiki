Developer guide
===============

.. toctree::
   :maxdepth: 1

   hatch
   environment
   testproject
   testing

.. highlight:: shell


Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/django-wiki/django-wiki/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Django-wiki could always use more documentation, whether as part of the
official django-wiki docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/django-wiki/django-wiki/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `django-wiki` for local development.

#. Fork the `django-wiki` repo on GitHub.
#. Clone your fork locally::

    $ git clone git@github.com:your_name_here/django-wiki.git

#. Go to your fork and install ``hatch`` which is the tool we use manage django-wiki
#. Install your local copy into a new environment. Assuming you have ``hatch`` installed, this is how you set up your fork for local development::

    $ cd django-wiki/
    $ hatch env create

#. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

#. As you are making changes you may want to verify that changes are
   passing all the relevant functional/unit tests::

    $ hatch run test:all

#. If you made changes related to the style sheets (SCSS), you need to install `sassc <https://sass-lang.com/libsass>`__ (``sudo apt install sassc``) and run this to compile css::

    $ hatch run assets

#. When you're done making changes, perform one final round of
   testing, and also ensure relevant tests pass with all supported
   Python versions with our matrix::

    $ hatch run test
    $ hatch run test:all # Runs all tests that pytest would run, just with various Python/Django combinations

#. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

#. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.6, 3.7, 3.8 and for PyPy. Check
   the status messages that are automatically generated for your pull request.

Tips
----

To run a subset of tests::

    $ hatch run test:all tests/core/test_basic.py # All tests from a single file.
    $ hatch run test:all tests/core/test_basic.py::URLPathTests # All tests from a single class.
    $ hatch run test:all tests/core/test_basic.py::URLPathTests::test_manager # Just one test.


Roadmap
-------

The best way to contribute is to use our Github issue list to look
at current wishes. The list is found here:

https://github.com/django-wiki/django-wiki/issues/

If you want to add a feature, consider writing a plugin. Please create an
issue to discuss whether your plugin idea is a core plugin
(``wiki.plugins.*``) or external plugin. If there are additions needed
to the plugin API, we can discuss that as well! A discussion is always welcome
in a Github issue.

Generally speaking, we need more **unit tests** to improve coverage, and new
features will not be accepted without tests. To add more stuff to the project
without tests wouldn't be fair to the project or your hard work. We use coverage
metrics to see that each new contribution does not significantly impact test
coverage.
