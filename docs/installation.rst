Installation
============

Pre-requisite: Pillow
---------------------

For image processing, django-wiki uses the `Pillow
library <https://github.com/python-pillow/Pillow>`_ (a fork of PIL).
The preferred method should be to get a system-wide, pre-compiled
version of Pillow, for instance by getting the binaries from your Linux
distribution repos.

Debian/Ubuntu
~~~~~~~~~~~~~

You need to get development libraries which Pip needs for compiling::

    sudo apt-get install libjpeg8 libjpeg-dev libpng12-0 libpng12-dev


After that, install with ``sudo pip install Pillow``. You might as well
install Pillow system-wide, because there are little version-specific
dependencies in Django applications when it comes to Pillow, and having
multiple installations of the very same package is a bad practice in
this case.

Mac OS X 10.5+
~~~~~~~~~~~~~~

`Ethan
Tira-Thompson <http://ethan.tira-thompson.com/Mac_OS_X_Ports.html>`_ has
created ports for OS X and made them available as a .dmg installer.
Download and install the universal combo package
`here <http://ethan.tira-thompson.com/Mac_OS_X_Ports_files/libjpeg-libpng%20%28universal%29.dmg>`_.

Once you have the packages installed, you can proceed to the pip
installation. PIL will automatically pick up these libraries and compile
them for django use.

Installing
----------

To install the latest stable release::

    pip install wiki

Install the latest pre-release (alpha, beta or rc)::

    pip install --pre wiki

Upgrading
---------

Always read the :doc:`release_notes` for instructions on upgrading.

Configuration
-------------

Configure ``settings.INSTALLED_APPS``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following applications should be listed - NB! it's important to
maintain the order due to database relational constraints:

.. code-block:: python

    'django.contrib.sites.apps.SitesConfig',
    'django.contrib.humanize.apps.HumanizeConfig',
    'django_nyt.apps.DjangoNytConfig',
    'mptt',
    'sekizai',
    'sorl.thumbnail',
    'wiki.apps.WikiConfig',
    'wiki.plugins.attachments.apps.AttachmentsConfig',
    'wiki.plugins.notifications.apps.NotificationsConfig',
    'wiki.plugins.images.apps.ImagesConfig',
    'wiki.plugins.macros.apps.MacrosConfig',


Database
~~~~~~~~

To sync and create tables, do:

::

    python manage.py migrate

Configure ``context_processors``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``django-wiki`` uses the `Django Templates` backend.
Add ``'sekizai.context_processors.sekizai'`` and ``'django.template.context_processors.debug'`` to
``context_processors`` section of your template backend settings.
Please refer to the `Django templates docs <https://docs.djangoproject.com/en/1.11/topics/templates/#django.template.backends.django.DjangoTemplates/>`_
to see the current default setting for this variable.

.. code-block:: python

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            # ...
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.request',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.contrib.messages.context_processors.messages',
                    "sekizai.context_processors.sekizai",
                ],
            },
        },
    ]


Set ``SITE_ID``
~~~~~~~~~~~~~~~

If you're working with fresh Django installation, you need to set the SITE_ID

.. code-block:: python

    SITE_ID = 1


User account handling
~~~~~~~~~~~~~~~~~~~~~

There is a limited account handling included to allow users to sign up. Its
settings are shown below with their default values. To switch off account
handling entirely, set ``WIKI_ACCOUNT_HANDLING = False``.

.. code-block:: python

    WIKI_ACCOUNT_HANDLING = True
    WIKI_ACCOUNT_SIGNUP_ALLOWED = True

After a user is logged in, they will be redirected to the value of
``LOGIN_REDIRECT_URL``, which you can configure in your project settings to
point to the root article:

.. code-block:: python

    from django.core.urlresolvers import reverse_lazy
    LOGIN_REDIRECT_URL = reverse_lazy('wiki:get', kwargs={'path': ''})



Include urlpatterns
~~~~~~~~~~~~~~~~~~~

To integrate the wiki in your existing application, you should ensure the
following lines are included in your project's ``urls.py``.

.. code-block:: python

    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('notifications/', include('django_nyt.urls')),
        path('', include('wiki.urls'))
    ]


The above line puts the wiki in */* so it's important to put it at the
end of your urlconf. You can also put it in */wiki* by putting
``'^wiki/'`` as the pattern.

.. note::

    If you are running ``manage.py runserver``, you need to have static files
    and media files from ``STATIC_ROOT`` and ``MEDIA_ROOT`` served by the
    development server. ``STATIC_ROOT`` is automatically served, but you have
    to add ``MEDIA_ROOT`` manually::

        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    Please refer to
    `the Django docs <https://docs.djangoproject.com/en/1.8/howto/static-files/#serving-files-uploaded-by-a-user-during-development>`__.
