Roadmap to RC1...
==============================

Unfinished
----------

 * Docs
 * Notification system **Almost done** (email notifications)
 * Circuit Editor plugin
 * Example plugin
 * Spam protection / Bot editing detection. Don't let anyone edit more than once every other minute.
 * Key-value meta data
 * Searching - Add Haystack detection
 * "Are you sure you want to leave this page" confirmation for Edit page.
 * Finish all class-based views **Almost Done**
 * Embeddable article template tag
 * "Fix Wiki URL bug in the footnotes plugin for python-markdown" ?
 * CodeMirror to be distributed with default setup
 
### Management script

 * Cleanup deleted Image's image files **Done**
 * Cleanup attachments **Done**
 * Cleanup revisions + plugin revisions
 * django_notify: send out email notifications **Done**

Done
----

 * Implement notifications, revision log messages and user messages thoroughly **Pretty much done**
 * View source for read-only articles + locked status **Done**
 * Index views for urlpaths **Done**
 * Permission system in settings tab **Done**
 * Special view for deleted articles w/ restore button **Done**
 * Article deletion **Done**
 * Image plugin **Done**
 * Attachment plugin **Done**
 * Simple user account handling: login/register etc. **Done**
 * South migrations **Done**
 * Custom storage engine for attachments **Done**
 * Handling WikiLinks and detecting broken links in markdown extension **Done**
 
Ideas
-----

 * Build menus of hierarchies and use bootstrap scrollspy. Add through plugin.
 * Notification system should be its own separate app
 * Statistics page for wiki owners
 * Table plugin: Quickly add a row of data to an existing table and sort data.
 * Auto-merge for conflicting concurrent revisions **Done**
 * Add revision conflict detection for concurrent editing **Done**
 * Make a comments plugin for commenting inline

Not planned
-----------

* Make dependency on django_notify optional
