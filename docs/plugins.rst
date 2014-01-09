Plugins
=======

Add/remove the following to your ``settings.INSTALLED_APPS`` to
enable/disable the core plugins:

-  ``'wiki.plugins.attachments'``
-  ``'wiki.plugins.images'``
-  ``'wiki.plugins.notifications'``

The notifications plugin is mandatory for an out-of-the-box installation. You
can safely remove it from ``INSTALLED_APPS`` if you also override the
**wiki/base.html** template.
