Tests
=====

Running tests
-------------

To run django-wiki's tests, run ``make test`` or ``pytest``

If you want to test for more **environments**, install "tox"
(``pip install tox``) and then just run ``tox`` to run the test
suite on multiple environments.

To run **specific tests**, see ``pytest --help``.

To include Selenium tests, you need to have ``Xvfb`` installed
(usually via system-provided package manager), `chromedriver
<https://sites.google.com/a/chromium.org/chromedriver/>`_ and set the
environment variable ``INCLUDE_SELENIUM_TESTS=1``. For example, run
tests with (depending on whether you want to test directly or via
tox)::

  INCLUDE_SELENIUM_TESTS=1 pytest
  INCLUDE_SELENIUM_TESTS=1 tox

If you wish to also show the browser window while running the
functional tests, set the environment variable
``SELENIUM_SHOW_BROWSER=1`` in *addition* to
``INCLUDE_SELENIUM_TESTS=1``, for example::

  INCLUDE_SELENIUM_TESTS=1 SELENIUM_SHOW_BROWSER=1 pytest


Writing tests
-------------

Tests generally fall into a few categories:

* Testing at the model level. These test cases should inherit from
  ``tests.base.TestBase``.

* Tests for views that return HTML. We normally use `django-functest
  <http://django-functest.readthedocs.io/en/latest/>`_ for these, especially if
  the page involves forms and handling of POST data. Test cases should inherit
  from ``tests.base.WebTestBase`` and ``tests.base.SeleniumBase`` - see
  ``tests.core.test_views.RootArticleViewTestsBase``,
  ``RootArticleViewTestsWebTest`` and ``RootArticleViewTestsSelenium`` for an
  example.

  (In the past the Django test Client was used for these, and currently there
  are still a lot of tests written in this style. These should be gradually
  phased out where possible, because the test Client does a poor job of
  replicating what browsers and people actually do.

* Tests for views that return JSON or other non-HTML. These test cases
  should inherit from ``tests.base.DjangoClientTestBase``.

There are also other mixins in ``tests.base`` that provide commonly used
fixtures for tests e.g. a root article.

.. warning::
  Views should be written so that as far as possible they work without
  Javascript, and can be tested using the fast WebTest method, rather than
  relying on the slow and fragile Selenium method. Selenium tests are not run by
  default.
