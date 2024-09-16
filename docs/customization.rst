Customization
=============

See :doc:`settings` for the settings that can be used to configure
django-wiki. Other ways to customize django-wiki for your use are listed below.

Templates
---------

django-wiki can be customized by providing your own templates.

All templates used by django-wiki inherit from ``wiki/base.html``, which in
turn simply inherits from ``wiki/base_site.html`` (adding
nothing). ``wiki/base_site.html`` provides a complete HTML page, but provides a
number of blocks that you might want to override. The most useful are:

* ``wiki_site_title``
* ``wiki_header_branding``
* ``wiki_header_navlinks``

These can be overridden to provide your own branding and links in the top bar of
the page, as well as in browser window title. The ``wiki/base_site.html``
template uses Bootstrap 3, so the following example shows how to use this in
practice, assuming you want a single link to your home page, and one to the
wiki. Add the following as ``wiki/base.html`` somewhere in your
``TEMPLATE_DIRS``:

.. code-block:: html+django

   {% extends "wiki/base_site.html" %}

   {% block wiki_site_title %} - Wiki{% endblock %}

   {% block wiki_header_branding %}
   <a href="{% url 'wiki:root' %}" class="d-flex align-items-center mb-2 mb-lg-0 link-body-emphasis text-decoration-none">
      <img height="40" class="me-2" src="{% static 'wiki/img/django-wiki-logo.svg' %}">
   </a>
   <a class="navbar-brand" href="/">Your brand</a>
   {% endblock %}

   {% block wiki_header_navlinks %}
     <li><a href="https://django-wiki.org" class="nav-link px-2 link-secondary">django-wiki</a></li>
   {% endblock %}

Site
----

You can override default django-wiki ``wiki.sites.site`` urls/views site implementation
with your own: override by setting the :attr:`~.WikiConfig.default_site` attribute
of a custom ``AppConfig`` to the dotted import path of either a ``WikiSite`` subclass
or a callable that returns a site instance.

.. code-block:: python

    # myproject/sites.py

    from wiki.sites import WikiSite

    class MyWikiSite(admin.WikiSite):
        ...

.. code-block:: python

    # myproject/apps.py

    from wiki.apps import WikiConfig

    class MyWikiConfig(WikiConfig):
        default_site = 'myproject.sites.MyWikiSite'

.. code-block:: python

    # myproject/settings.py

    INSTALLED_APPS = [
        ...
        'myproject.apps.MyWikiConfig',  # replaces 'wiki.apps.WikiConfig'
        ...
    ]
