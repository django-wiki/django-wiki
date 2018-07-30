Plugins
=======

Add/remove the following to your ``settings.INSTALLED_APPS`` to
enable/disable the core plugins:

-  ``'wiki.plugins.attachments.apps.AttachmentsConfig'``
-  ``'wiki.plugins.globalhistory.apps.GlobalHistoryConfig'``
-  ``'wiki.plugins.help.apps.HelpConfig'``
-  ``'wiki.plugins.images.apps.ImagesConfig'``
-  ``'wiki.plugins.links.apps.LinksConfig'``
-  ``'wiki.plugins.macros.apps.MacrosConfig'``
-  ``'wiki.plugins.notifications.apps.NotificationsConfig'``

The notifications plugin is mandatory for an out-of-the-box installation. You
can safely remove it from ``INSTALLED_APPS`` if you also override the
**wiki/base.html** template.
