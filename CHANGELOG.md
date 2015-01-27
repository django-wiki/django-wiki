Latest Changes
==============
Compiled on: Mon Jan 26 2015

    * 67e9d40	Benjamin Bach	2015-01-26	version bump to 0.0.24
    * 0dd77b8	Benjamin Bach	2015-01-26	0.0.24 migrations applied to test database
    * 228cb96	Benjamin Bach	2015-01-26	Do not have MANIFEST.in as a symlink, does not work in distributed zip archives
    * 28561ea	Benjamin Bach	2015-01-26	make new table renaming migrations python3 compatible #290
    * 311f7ce	Benjamin Bach	2015-01-26	Output end result when creating articles and make py3 ready
    * 11cc61e	Benjamin Bach	2015-01-26	Rename the migration that restores the table in case its already marked as run
    * c232ada	Benjamin Bach	2015-01-26	Rename notifications_... tables to wiki_notifications_... #290
    * 28c55a4	Benjamin Bach	2015-01-26	Remove unused models module
    * bec089b	Benjamin Bach	2015-01-26	Rename attachments_... tables to wiki_attachments_... #290
    * ff14161	Benjamin Bach	2015-01-26	change table names on images plugin #290
    * 896a133	Benjamin Bach	2015-01-26	conditionally create the articlenotifications table if it doesnt exist because of the old broken migration
    * d248b9d	Benjamin Bach	2015-01-26	add empty migration in place of old broken migration from 0.23
    * 70e295d	Benjamin Bach	2015-01-26	note on markdown 2.3
    *   1cdf0b4	benjaoming	2015-01-26	Merge pull request #372 from Alkalit/master
    |\  
    | * 1689f3b	Alkalit	2015-01-26	future import moved to file top.
    |/  
    *   ffe4b81	Benjamin Bach	2015-01-08	Upgrading to newest bootstrap and font awesome - thanks @cXhristian!!
    |\  
    | * f053c15	Christian Duvholt	2015-01-08	Add horizontal scrolling to big diffs. Fixed accordion heading CSS.
    | * 515b6cd	Christian Duvholt	2015-01-08	Fix history diff collapse
    | * 1e79e72	Christian Duvholt	2015-01-07	Fix navbar collapse
    | * 255c52c	Christian Duvholt	2015-01-07	Fix vertical align on typeahead input group
    | * 2e4d49c	Christian Duvholt	2015-01-07	Upgrade to Font Awesome 4
    | * 271431b	Christian Duvholt	2015-01-07	Update templates for Bootstrap 3.3.1. Fix modals and search.
    | * b3ccbdd	Christian Duvholt	2015-01-06	Upgraded Bootstrap files to 3.3.1
    * |   3561b2a	benjaoming	2015-01-07	Merge pull request #357 from cXhristian/preview-markdown
    |\ \  
    | * | 4ff8baf	Christian Duvholt	2014-11-25	Created a new core markdown extension folder. Moved preview links extension.
    | * | 29d0013	Christian Duvholt	2014-11-23	Set <a target="_blank"> for all links when in preview mode. Fixes #256.
    * | |   7b87e84	benjaoming	2015-01-07	Merge pull request #367 from orblivion/patch-3
    |\ \ \  
    | |_|/  
    |/| |   
    | * | 12920af	orblivion	2015-01-06	Properly sets default configs in plugins/links/mdx
    |/ /  
    * | 9a08694	Benjamin Bach	2015-01-06	new demo site url
    * | e9332ca	Benjamin Bach	2015-01-06	rtfd badge
    * | b3affd7	Benjamin Bach	2015-01-06	build LESS files for fix of input type=email
    * | 18c2f12	Benjamin Bach	2015-01-06	fix migrations in testproject database
    * | 1de0f20	Benjamin Bach	2015-01-06	Better guidance for upgrading and notifications issue #288
    * | 1965d0a	Benjamin Bach	2015-01-06	Fix up creating default subscriptions, realted to #288
    * | 117727a	Benjamin Bach	2015-01-06	warn about not having changed to django_nyt
    * | c8961f3	Benjamin Bach	2015-01-06	typo and code format
    * | c7ebf2f	Benjamin Bach	2015-01-05	Add input[type=email] - fixes #363
    * | 8f2ef2b	Benjamin Bach	2015-01-05	Make Bootstrap/LESS customization easier by putting all custom wiki styles in their own LESS file and not mingle them with the Bootstrap import statement - fixes #364
    * |   9976b29	benjaoming	2014-11-26	Merge pull request #360 from orblivion/patch-1
    |\ \  
    | * | 9c14f86	orblivion	2014-11-26	tips.rst - typeo
    |/ /  
    * | 2fee7db	benjaoming	2014-11-25	cannot concatenate a tuple
    * |   24764e3	benjaoming	2014-11-24	Merge pull request #358 from spookylukey/synchronise_travis_and_tox_2
    |\ \  
    | * | 52cba45	Luke Plant	2014-11-22	Properly synchronised tox and travis test config
    |/ /  
    * |   b8fae91	benjaoming	2014-11-23	Merge pull request #353 from spookylukey/fix_module_name_deprecation
    |\ \  
    | |/  
    |/|   
    | * c8ec345	Luke Plant	2014-11-22	Fixed dependencies in tox.ini so that tests run
    | * 5cb503d	Luke Plant	2014-11-22	Fixed deprecation warnings issues by migrations.
    |/  
    *   40b0e5d	benjaoming	2014-11-22	Merge pull request #352 from cXhristian/notifications-subscription-fix
    |\  
    | * e3e00ec	Christian Duvholt	2014-11-22	Fix #265
    |/  
    *   843225c	benjaoming	2014-11-19	Merge pull request #351 from cXhristian/plugins-unicode
    |\  
    | * 6e4f957	Christian Duvholt	2014-11-19	Add use __str__ with python_2_unicode_compatible for plugins too
    |/  
    *   ab8bf24	benjaoming	2014-11-19	Merge pull request #349 from django-wiki/revert-347-plugins-unicode
    |\  
    | * fd9bb87	benjaoming	2014-11-19	Revert "Add use __str__ with python_2_unicode_compatible for plugins too"
    |/  
    *   588e693	benjaoming	2014-11-19	Merge pull request #347 from cXhristian/plugins-unicode
    |\  
    | * bb3b337	Christian Duvholt	2014-11-19	Add use __str__ with python_2_unicode_compatible for plugins too
    |/  
    *   0d012c7	benjaoming	2014-11-18	Merge pull request #346 from jandebleser/master
    |\  
    | * 87f964a	Jan De Bleser	2014-11-18	Fixed problem with cleaning the username when the application is using a custom username field.
    |/  
    *   e9495a8	benjaoming	2014-11-16	Merge pull request #345 from cXhristian/attachment-fixes
    |\  
    | * b46ced1	Christian Duvholt	2014-11-16	Better messages when adding attachments
    | * 5f58fdf	Christian Duvholt	2014-11-16	Clear cache for article when doing something with attachments
    | * 25e8a47	Christian Duvholt	2014-11-16	Fix many issues with attachments caused by attachment-filter not being specifc enough
    | * 16a6894	Christian Duvholt	2014-11-16	Fix not being able to add existing attachments to an article
    | * f8eb556	Christian Duvholt	2014-11-16	Fix broken markdown output when attachment does not exist
    |/  
    *   c7f8ff0	benjaoming	2014-11-14	Merge pull request #343 from cXhristian/settings-subscriptions-count
    |\  
    | * abd304b	Christian Duvholt	2014-11-14	Fix notification error in settings
    |/  
    * 579c67e	paul	2014-11-13	Adding python_2_unicode_compatible from @fsx999, #Fix 282 and Close #342
    * 62d67c0	benjaoming	2014-11-13	Fix #341
    * c551a69	benjaoming	2014-11-13	Fix #263 and style article list header
    * 93464ba	benjaoming	2014-11-13	add more tests of custom managers and add support for django 1.5 and 1.6's patterns for empty querysets
    * 294839e	benjaoming	2014-11-13	use gettext_lazy where appropriate, thanks @jluttine for starting work on this
    *   fa01cfb	benjaoming	2014-11-12	Merge pull request #337 from fsx999/master
    |\  
    | * e56a78a	paul	2014-11-06	python_2_unicode_compatible decorateur
    * | 97b4a32	benjaoming	2014-11-12	add tests of none() and empty queryset functionality
    * | 71f2693	benjaoming	2014-11-12	do not call get_empty_query_set, that's deprecated
    * | d11a036	benjaoming	2014-11-12	initial tests for custom queryset methods
    * | f2c2d4d	benjaoming	2014-11-12	ignore wiki/attachments for now as it occurs from running tests and should not be distributed
    * | 7a47924	benjaoming	2014-11-12	pep8
    * |   6a76e16	benjaoming	2014-11-12	Merge pull request #338 from cXhristian/future-import-fix
    |\ \  
    | |/  
    |/|   
    | * bfcda5f	Christian Duvholt	2014-11-12	Move future import to the top
    |/  
    *   0d10395	benjaoming	2014-11-06	Merge branch 'kilrogg-master' PR#309
    |\  
    | *   7bb4334	benjaoming	2014-11-06	Merge branch 'master' of github.com:kilrogg/django-wiki into kilrogg-master
    | |\  
    | | * aded511	Benjamin Richter	2014-10-10	% fix haystack search query (request.group not set and should be list of all groups)
    | | * bddeb12	Benjamin Richter	2014-10-10	% fix saving of notification settings
    | | * 7010312	Benjamin Richter	2014-10-10	% fix notifications overview
    * | |   93049a3	benjaoming	2014-11-04	Merge pull request #325 from jluttine/fix-testproject-manage
    |\ \ \  
    | * | | 3d70212	Jaakko Luttinen	2014-11-02	Fix testproject/manage.py to be executable
    * | | |   60bf09e	benjaoming	2014-11-03	Merge pull request #327 from jluttine/fix-326-search-title
    |\ \ \ \  
    | |_|/ /  
    |/| | |   
    | * | | f83effc	Jaakko Luttinen	2014-11-02	Fix issue #326
    | |/ /  
    * | | f100e69	benjaoming	2014-11-03	Remove Python 3.2 testing because South migrations arent running
    * | |   99c8d6b	benjaoming	2014-11-03	Merge pull request #330 from spookylukey/reset_notifications_migrations
    |\ \ \  
    | * | | 38c0007	Luke Plant	2014-11-03	Migrations reset on the rather messed up notifications app
    * | | | cf96c61	benjaoming	2014-11-03	add note on master branch
    * | | |   7087775	benjaoming	2014-11-03	Merge pull request #332 from spookylukey/fix_upload_for_python3_rebased
    |\ \ \ \  
    | * | | | 197bd20	Luke Plant	2014-10-01	Fixed uploading of attachments using Python3
    | * | | | 61ffee0	Luke Plant	2014-10-01	Removed stray debugging print statement
    | * | | | c1b2408	Luke Plant	2014-10-01	Fixed bug with caching that was causing a test to fail.
    | * | | | 844bbd4	Luke Plant	2014-10-01	Pulled out some useful base classes for test cases
    | * | | | 13502c6	Luke Plant	2014-10-01	Get tests to run under Django 1.4 and 1.5, but without duplication on 1.6 and later
    | * | | | 57df9c4	Luke Plant	2014-10-01	Updated dependencies in tox.ini to latest supported versions of Django
    | * | | | 8145c45	Luke Plant	2014-10-01	Tests should be run against current version of django-wiki, not old version!
    | | |/ /  
    | |/| |   
    * | | |   1d5c033	benjaoming	2014-11-03	Merge pull request #331 from spookylukey/fix_hashbangs
    |\ \ \ \  
    | |/ / /  
    |/| | |   
    | * | | f77220e	Luke Plant	2014-11-03	Fixed runtests.py and setup.py hashbang lines, broken by commit with python-modernizer
    |/ / /  
    * | | c91061a	benjaoming	2014-10-28	Fix #295
    |/ /  
    * | 4549941	benjaoming	2014-10-28	use python-modernizer to fix migrations and other small issues
    * | 43ce281	benjaoming	2014-10-28	Update travis config, remove django 1.4 stuff
    * | bc7464d	benjaoming	2014-10-28	initial work on danish translation
    * | 2974f00	benjaoming	2014-10-28	update django-nyt requirement because of python3
    * | da57263	benjaoming	2014-10-28	python3 compat bug
    * | 1574c00	benjaoming	2014-10-26	remove django 1.7 from 0.0.24 travis tests
    * |   35c7496	benjaoming	2014-10-26	Merge pull request #322 from jluttine/finnish-translation
    |\ \  
    | * | 90e8443	Jaakko Luttinen	2014-10-26	Preliminary Finnish translation
    * | |   2e8d918	benjaoming	2014-10-26	Merge pull request #321 from jluttine/fix-requirements
    |\ \ \  
    | |/ /  
    |/| |   
    | * |   70e78eb	Jaakko Luttinen	2014-10-26	Merge pull request #1 from django-wiki/jluttine-fix-requirements
    | |\ \  
    | | * | bfe7544	benjaoming	2014-10-26	add traceback to reveal why errors in the testing framework occurs
    | |/ /  
    | * | 8e4cce9	Jaakko Luttinen	2014-10-26	Fix Django v1.7 in Travis file
    | * | 5a97d1a	Jaakko Luttinen	2014-10-26	Remove a debugging message that was left accidentally
    | * | 17a6890	Jaakko Luttinen	2014-10-26	Fix South requirement to >=0.8.4
    | * | 67f7ae9	Jaakko Luttinen	2014-10-26	Refactor dependencies in requirements.txt and setup.py
    | * | 9e0c9a7	Jaakko Luttinen	2014-10-26	Fix South handling in requirements
    | * | 7f20035	Jaakko Luttinen	2014-10-26	Fix Python 2.6 error caused by Markdown updates
    | * | ae85033	Jaakko Luttinen	2014-10-26	Share common requirements for Travis and distribution (fix #319)
    |/ /  
    * |   55eb10a	benjaoming	2014-10-25	Merge pull request #317 from jluttine/fix-travis-mptt
    |\ \  
    | * | 181435c	Jaakko Luttinen	2014-10-25	Fix Travis CI requirements to use django-mptt==0.6.0
    |/ /  
    * |   f380852	benjaoming	2014-10-24	Merge pull request #316 from jluttine/fix-travis-url
    |\ \  
    | * | 84c07fb	Jaakko Luttinen	2014-10-24	Fix Travis-CI URL in README
    |/ /  
    * |   d88db48	benjaoming	2014-10-23	Merge pull request #315 from norkans7/small_fix
    |\ \  
    | * | 81a3273	Norbert Kwizera	2014-10-23	fix css class name
    * | |   3754835	benjaoming	2014-10-23	Merge pull request #314 from jluttine/master
    |\ \ \  
    | |/ /  
    |/| |   
    | * | 9d411a7	Jaakko Luttinen	2014-10-23	Change empty markdown config to {} instead of None
    |/ /  
    * |   cff1f74	benjaoming	2014-10-16	Merge pull request #313 from jandebleser/master
    |\ \  
    | * | 43d94e6	Jan De Bleser	2014-10-16	Fixed problem with auth.user in the south migrations for plugin 'images'.
    |/ /  
    * |   c007ca9	benjaoming	2014-10-15	Merge pull request #312 from jandebleser/master
    |\ \  
    | |/  
    |/|   
    | * c618f57	Jan De Bleser	2014-10-15	Fixed problem with auth.user in the south migrations. Further continuation of e506c0941bfed1104394ffc176484c928685080f.
    |/  
    *   ffe9c87	benjaoming	2014-10-06	Merge pull request #307 from spookylukey/master
    |\  
    | * 4ec26b2	Luke Plant	2014-10-01	Python 3 compatibility (or at least correct syntax) for mediawikimport command
    |/  
    *   7c10ab9	benjaoming	2014-09-19	Merge pull request #303 from thanhleviet/patch-1
    |\  
    | * 5913634	Thanh Lê	2014-09-19	Update installation.rst
    |/  
    *   da653dc	benjaoming	2014-09-10	Merge pull request #301 from Fantomas42/patch-1
    |\  
    | * 036311f	Julien Fache	2014-09-10	Update .travis.yml
    |/  
    *   16063db	benjaoming	2014-09-09	Merge pull request #300 from pknowles/master
    |\  
    | * 20041bd	pknowles	2014-09-10	Updated setting name ALLOW_OVERLAPPING_THIRD_PARTY_URL to CHECK_SLUG_URL_AVAILABLE
    | * 9eae449	pknowles	2014-09-10	Added validation for slugs conflicting with 3rd party URLs, and option to disable with ALLOW_OVERLAPPING_THIRD_PARTY_URL = True
    |/  
    *   20748ad	benjaoming	2014-09-07	Merge pull request #299 from tkliuxing/master
    |\  
    | * a50a5cf	Ronald Bai	2014-09-08	Add Simplified Chinese translation.
    |/  
    * d0a83ce	benjaoming	2014-08-30	Updating model chart. Command used:
    * b759c5b	benjaoming	2014-08-13	give at least anon ready access to front page
    * 64636dc	benjaoming	2014-08-13	update test database and make front page only editable by admin
    * 74871db	benjaoming	2014-07-31	Add a bit more info, and thanks @almereyda for noticing.
    * bccd5b6	benjaoming	2014-08-02	Add IRC notifications
    *   4c3d557	benjaoming	2014-07-27	Merge pull request #293 from clincher/patch-1
    |\  
    | * e5fbd6b	Василий	2014-07-27	Update markdown_extensions.py
    |/  
    * ba21cc0	benjaoming	2014-07-23	increase django-nyt version dep
    * aec9c1e	benjaoming	2014-07-23	fix wrongly resetting notification badge color at every update
    * 25ee8b7	benjaoming	2014-07-21	Add missing migration for deleted field Image.image - Fixes #281
    * 1ce1928	benjaoming	2014-07-19	docs change on how to handle notifications for 0.0.24
    * 5dd9a98	benjaoming	2014-07-19	dependency on new django_nyt
    * eea0c43	benjaoming	2014-07-19	notifications plugin form to use django-nyt and management command to recreate notifications
    *   6f13af4	benjaoming	2014-07-19	Merge pull request #289 from django-wiki/revert-272-fix_224
    |\  
    | * 84f7508	benjaoming	2014-07-19	Revert "Fix #224"
    |/  
    * 1ec4e74	benjaoming	2014-07-19	do not install django-mptt 0.6.1 it's broken
    * 178aa26	benjaoming	2014-07-19	more info on new releases
    * eac7504	benjaoming	2014-07-18	Fix #270
    *   25f2cd5	benjaoming	2014-07-18	Merge pull request #279 from SacNaturalFoods/update-help-plugin
    |\  
    | * d404a15	tschmidt	2014-06-25	corrected lists section of help plugin for sub items
    * | 1614eb5	benjaoming	2014-07-18	add missing paragraph
    * | 9ff1ab9	benjaoming	2014-07-18	add note about django-wiki-project-template
    * | a7acc42	benjaoming	2014-05-26	pep8
    * |   bacba8d	benjaoming	2014-07-12	Merge pull request #269 from fangsterr/master
    |\ \  
    | * | 5521c3b	Andy Fang	2014-06-17	article settings form compatibility with custom user model
    * | |   8a7f288	benjaoming	2014-07-08	Merge pull request #278 from PolyLAN/fix_262
    |\ \ \  
    | * | | 1445ad5	Maximilien Cuony	2014-06-23	Fix #262 for attachements
    | |/ /  
    * | |   9100c42	benjaoming	2014-07-08	Merge pull request #272 from PolyLAN/fix_224
    |\ \ \  
    | * | | 4e7031d	Maximilien Cuony	2014-06-19	Also fix in the plugin
    | * | | fdb6ba8	Maximilien Cuony	2014-06-19	Typo, nty->nyt
    | * | | 8646f11	Maximilien Cuony	2014-06-19	Rename notify to nyt (https://github.com/benjaoming/django-wiki/issues/224#issuecomment-44047813=
    | |/ /  
    * | |   daf13cf	benjaoming	2014-07-08	Merge pull request #273 from PolyLAN/fix_haystack_confict
    |\ \ \  
    | * | | 5754e97	Maximilien Cuony	2014-06-19	Test the presence of the plugin haystack, not haystack himself
    | |/ /  
    * | |   d0e77d0	benjaoming	2014-07-08	Merge pull request #275 from PolyLAN/mediawiki_import
    |\ \ \  
    | |/ /  
    |/| |   
    | * | 9c5e6b0	Maximilien Cuony	2014-06-21	Better import: Expend templates, better url handeling and internal links
    | * | c4fce27	Maximilien Cuony	2014-06-20	Import mediawiki: First basic version. * Import page, with history and users
    |/ /  
    * |   2671dbf	benjaoming	2014-06-16	Merge pull request #267 from daonb/master
    |\ \  
    | * | c415572	Benny Daon	2014-06-16	Fix testproject instructions
    |/ /  
    * | 3125d7d	benjaoming	2014-05-27	Add explanation of current build status.
    * | f1a4aa6	benjaoming	2014-05-21	Travis should not test Django 1.4 against Python 3
    * | 9f265e5	benjaoming	2014-05-21	Fix #234 by adding @friedmud's suggestion and a max-height om <pre>'s
    * | 44dcfdd	benjaoming	2014-05-20	Fix filter() call in get_content_snippet not working on Python 2.7+
    * | e60cae5	benjaoming	2014-05-20	Adding prepopulated DB with front page article
    * |   8c45e4a	benjaoming	2014-05-20	Merge branch 'mastak-master'
    |\ \  
    | * \   c971cb4	benjaoming	2014-05-20	Merge branch 'master' of github.com:mastak/django-wiki into mastak-master
    | |\ \  
    |/ / /  
    | * | 6323f81	Lubimov Igor	2014-05-06	replcae ArticleEmptyQuerySet to query_set().none(). Django 1.6 compatibilty
    * | | d6cf63f	benjaoming	2014-05-19	once again correcting travis config and adding py3 fixed requirement for django_nyt
    * | | aa2980d	benjaoming	2014-05-19	travis pip syntax err
    * | | 53fda7f	benjaoming	2014-05-19	Only Django 1.4.2+ is support because of django-mptt
    * | | 3d37d9f	benjaoming	2014-05-19	Only Django 1.4.2+ is support because of django-mptt
    * | | a219296	benjaoming	2014-05-19	Add list of known issues and include a note on Dj 1.4 and sorl with that.
    * | | abbacee	benjaoming	2014-05-19	fix travis syntax err
    * | | 53cf3dc	benjaoming	2014-05-19	Reconstructing Travis YML to only use selected combinations of django and python versions
    * | | 8dbcc7d	benjaoming	2014-05-19	Travis requirements to get sorl 11.12.1b and fix django 1.7 beta from tarball instead of pip
    * | | 1c01ed8	benjaoming	2014-05-19	start testing south migrations again
    * | | 25a0206	benjaoming	2014-05-19	Fix broken images.south_migrations (0001_initial), add new .travis requirements
    * | | d1aeea8	benjaoming	2014-05-18	Adding draft notice to release notes
    * | |   9e518c2	benjaoming	2014-05-18	Merge branch 'master' of github.com:benjaoming/django-wiki
    |\ \ \  
    | * | | 3fc6745	benjaoming	2014-05-18	removing migration testing for now due to unknown erro
    * | | | fa16ac3	benjaoming	2014-05-18	removing migration testing for now due to unknown error
    |/ / /  
    * | | 9221c15	benjaoming	2014-05-18	add release note link
    * | | cf789ec	benjaoming	2014-05-18	(Missing from previous commit)
    * | | ddf6aa3	benjaoming	2014-05-18	Refactor old South migration modules "migrations"->"south_migrations", add AppConfigs for future Django 1.7 (not supported yet), initial release notes, delete odd notifications migration that by mistake deletes the notifications subscriptions tables!
    * | | 102b015	benjaoming	2014-05-18	south migration and django 1.7 transitional support, remove django_notify and use django_nyt
    * | | bb82b46	benjaoming	2014-05-17	Tests should reflect forced lowercase paths.
    * | |   b032b61	benjaoming	2014-05-17	Merge branch 'master' of github.com:benjaoming/django-wiki
    |\ \ \  
    | * | | 8c45335	benjaoming	2014-05-07	Update article.py
    | * | | 4783abd	benjaoming	2014-05-07	Only force new slugs to lowercase when not URL_CASE_SENSITIVE
    | * | | 42b6c49	benjaoming	2014-05-07	Fix confusing comment
    | * | |   7d45a29	benjaoming	2014-05-07	Merge pull request #260 from Jayflux/fixing_hyphen
    | |\ \ \  
    | | |/ /  
    | |/| |   
    | | * | 682a217	Jason Williams	2014-05-05	added HTML5 pattern checking of lowercase and underscores
    | | * | 3488ef1	Jason Williams	2014-05-04	forcing cleanup server side
    | | * | 5ae09e6	Jason Williams	2014-04-29	fixing mistake made from last commit
    | | * | c84a4b4	Jason Williams	2014-04-29	This line should be removed, as it is removing the hyphen
    | |/ /  
    * | | 38dc640	benjaoming	2014-05-17	Make tests run on django<1.6
    * | |   efae942	benjaoming	2014-05-17	Merge branch 'python3' of github.com:benjaoming/django-wiki into python3
    |\ \ \  
    | * \ \   4040a48	benjaoming	2014-04-14	Merge pull request #254 from Mobeye/python3
    | |\ \ \  
    | | * | | d43557a	Antonin Lenfant	2014-04-11	Specified a version for sorl-thumbnails that is compatible with Python3
    | | * | | 5c3a470	Antonin Lenfant	2014-04-11	Fix image upload when IMAGE_PATH_OBSCURIFY setting is enabled
    | |/ / /  
    | * | |   ea3ef80	benjaoming	2014-03-24	Merge pull request #251 from spookylukey/python3
    | |\ \ \  
    | | * | | 08c2fd8	Luke Plant	2014-03-22	Fixed tox.ini dependencies for Python 3 support
    | | * | | d6eaf90	Luke Plant	2014-03-22	Added python3.3 environment to the envs to test in tox.ini
    | | * | | f1de262	Luke Plant	2014-03-22	Removed use of unicode_literals in migrations, because it causes many migrations to generate TypeError
    | | * | |   0eec72b	Luke Plant	2014-03-22	Merge branch 'master' into python3
    | | |\ \ \  
    | |/ / / /  
    | * | | | e66b853	Russell-Jones	2014-01-22	Move from __future__ to the beginning of the file
    | * | | |   fc91851	Russell-Jones	2014-01-14	Merge pull request #233 from benjaoming/master
    | |\ \ \ \  
    | * \ \ \ \   7b19154	Russell-Jones	2014-01-12	Merge pull request #231 from benjaoming/master
    | |\ \ \ \ \  
    | * | | | | | 90e5a7b	Russell-Jones	2014-01-11	Try change made by benjaoming on django-nyt
    | * | | | | | 7694ee4	Russell Jones	2014-01-11	Move to python3-style unicode everywhere str()
    | * | | | | | 29c4b56	Russell Jones	2014-01-11	Move to python3-style unicode everywhere str()
    | * | | | | | 18d0fc7	Russell-Jones	2014-01-11	Switch to python3-style unicode everywhere str()
    | * | | | | | 777b9aa	Russell-Jones	2014-01-10	Switch to python3-style unicode everywhere str()
    | * | | | | |   4fc7f57	Russell-Jones	2014-01-10	Merge pull request #229 from benjaoming/master
    | |\ \ \ \ \ \  
    | * | | | | | | 2fc0f26	Russell-Jones	2014-01-10	Switch to Pillow and the dev version of sorl v12
    | * | | | | | | e6e7343	Russell-Jones	2014-01-10	Add python 3.2 and 3.3 to trigger branch tci build
    | * | | | | | |   df496e9	Russell Jones	2014-01-06	Merge branch 'master' into python3
    | |\ \ \ \ \ \ \  
    | * | | | | | | | dba4b67	Russell Jones	2014-01-06	Convert filter iterator to list() to allow subscript
    | * | | | | | | | 5a61e76	Russell Jones	2014-01-06	Correct position of from future import
    | * | | | | | | | 77fd906	Russell Jones	2014-01-06	Start using from __future__ import unicode_literals everywhere Remove u from  u"" and u'' Start to remove calls to unicode()
    | * | | | | | | | 93abe74	Russell Jones	2014-01-06	Import only string_types from six
    | * | | | | | | | c9b32ae	Russell Jones	2014-01-06	Replace basestring with six.string_types
    | * | | | | | | | 58a3434	Russell Jones	2014-01-06	Try to work around (necessary) absence of force_unicode in Django on python 3
    | * | | | | | | | b2fc091	Russell Jones	2014-01-06	Add six to travis requirements.txt
    | * | | | | | | |   ce3d62e	benjaoming	2014-01-06	Merge branch 'py2and3' of github.com:Russell-Jones/django-wiki into python3
    | |\ \ \ \ \ \ \ \  
    | | * | | | | | | | 61d3f10	Russell Jones	2014-01-06	Stray tab
    | | * | | | | | | | 6255677	Russell Jones	2014-01-06	Convert iterator to list to allow extension with + operator
    | | * | | | | | | | c56224d	Russell Jones	2014-01-06	Add six as a requirement
    | | * | | | | | | | 8c4c091	Russell Jones	2014-01-06	Missing colon
    | | * | | | | | | | 8935aa0	Russell Jones	2014-01-06	Add changes suggested by python-modernize
    * | | | | | | | | | 3f88b01	benjaoming	2014-05-17	Fix py3 syntax error, refactor tests to be run with DiscoverRunner
    * | | | | | | | | | 77413fe	Antonin Lenfant	2014-04-11	Specified a version for sorl-thumbnails that is compatible with Python3
    * | | | | | | | | | d6ba371	Antonin Lenfant	2014-04-11	Fix image upload when IMAGE_PATH_OBSCURIFY setting is enabled
    * | | | | | | | | | 4c54b9a	Luke Plant	2014-03-22	Fixed tox.ini dependencies for Python 3 support
    * | | | | | | | | | 606592b	Luke Plant	2014-03-22	Added python3.3 environment to the envs to test in tox.ini
    * | | | | | | | | | 2e4f15c	Luke Plant	2014-03-22	Removed use of unicode_literals in migrations, because it causes many migrations to generate TypeError
    * | | | | | | | | | d82e3b1	Russell-Jones	2014-01-22	Move from __future__ to the beginning of the file
    * | | | | | | | | | a0d1862	Russell-Jones	2014-01-11	Try change made by benjaoming on django-nyt
    * | | | | | | | | | e9c244f	Russell Jones	2014-01-11	Move to python3-style unicode everywhere str()
    * | | | | | | | | | 4f9bf51	Russell Jones	2014-01-11	Move to python3-style unicode everywhere str()
    * | | | | | | | | | 2eb94b3	Russell-Jones	2014-01-11	Switch to python3-style unicode everywhere str()
    * | | | | | | | | | 20e567a	Russell-Jones	2014-01-10	Switch to python3-style unicode everywhere str()
    * | | | | | | | | | 1b06ace	Russell-Jones	2014-01-10	Switch to Pillow and the dev version of sorl v12
    * | | | | | | | | | 3ab06b2	Russell-Jones	2014-01-10	Add python 3.2 and 3.3 to trigger branch tci build
    * | | | | | | | | | a9b3b5d	Russell Jones	2014-01-06	Convert filter iterator to list() to allow subscript
    * | | | | | | | | | e8c1345	Russell Jones	2014-01-06	Correct position of from future import
    * | | | | | | | | | fd2475d	Russell Jones	2014-01-06	Start using from __future__ import unicode_literals everywhere Remove u from  u"" and u'' Start to remove calls to unicode()
    * | | | | | | | | | b74539f	Russell Jones	2014-01-06	Import only string_types from six
    * | | | | | | | | | 6ecb821	Russell Jones	2014-01-06	Replace basestring with six.string_types
    * | | | | | | | | | 1baf410	Russell Jones	2014-01-06	Try to work around (necessary) absence of force_unicode in Django on python 3
    * | | | | | | | | | 6be734f	Russell Jones	2014-01-06	Add six to travis requirements.txt
    * | | | | | | | | | d0d585b	Russell Jones	2014-01-06	Stray tab
    * | | | | | | | | | 4b5a928	Russell Jones	2014-01-06	Convert iterator to list to allow extension with + operator
    * | | | | | | | | | d88433d	Russell Jones	2014-01-06	Add six as a requirement
    * | | | | | | | | | 810581a	Russell Jones	2014-01-06	Missing colon
    * | | | | | | | | | 791888e	Russell Jones	2014-01-06	Add changes suggested by python-modernize
    * | | | | | | | | | a559f73	benjaoming	2014-04-11	typo
    | |_|_|_|_|_|_|/ /  
    |/| | | | | | | |   
    * | | | | | | | | 469d050	benjaoming	2014-04-01	notes on pull requests
    * | | | | | | | | 032b517	benjaoming	2014-04-01	Let us try adding a contribution documentent...
    | |_|_|_|_|_|/ /  
    |/| | | | | | |   
    * | | | | | | |   2340c32	benjaoming	2014-03-19	Merge pull request #250 from valberg/master
    |\ \ \ \ \ \ \ \  
    | * | | | | | | | 273b30c	valberg	2014-03-19	Update installation.rst
    | * | | | | | | | 4247d6a	valberg	2014-03-19	Fixing requirements list
    |/ / / / / / / /  
    * | | | | | | |   76306f1	benjaoming	2014-03-18	Merge pull request #249 from andyreagan/patch-2
    |\ \ \ \ \ \ \ \  
    | * | | | | | | | 134006e	Andy Reagan	2014-03-18	Update installation.rst
    * | | | | | | | |   e523e00	benjaoming	2014-03-18	Merge pull request #248 from andyreagan/patch-1
    |\ \ \ \ \ \ \ \ \  
    | |/ / / / / / / /  
    |/| | | | | | | |   
    | * | | | | | | | 5204edd	Andy Reagan	2014-03-18	Update installation.rst
    |/ / / / / / / /  
    * | | | | | | |   df22c9f	benjaoming	2014-02-12	Merge pull request #241 from spookylukey/fix_transaction_management
    |\ \ \ \ \ \ \ \  
    | * | | | | | | | 457c487	Luke Plant	2014-02-11	Merged wiki.compat into wiki.core.compat
    | * | | | | | | | 086a36c	Luke Plant	2014-02-04	Added tox.ini and instructions, for easy running of tests in multiple environments
    | * | | | | | | | 08312fc	Luke Plant	2014-02-03	Fix for issue #225 (exception when running with ATOMIC_REQUESTS), and the same applied to deleting subtrees
    | * | | | | | | | 26ce59d	Luke Plant	2014-02-03	Added method to allow selected tests to be run, instead of running all.
    | * | | | | | | | 6b300ac	Luke Plant	2014-02-03	Executable scripts 'setup.py' and 'runtests.py'
    | * | | | | | | | f414e4a	Luke Plant	2014-02-03	Fixed incorrect indentation
    | | |_|_|_|_|/ /  
    | |/| | | | | |   
    * | | | | | | | 8778a80	benjaoming	2014-02-12	Replace PIL with Pillow
    |/ / / / / / /  
    * | | | | | |   11728df	benjaoming	2014-01-14	Merge pull request #232 from vincentalvo/patch-1
    |\ \ \ \ \ \ \  
    | |_|_|_|_|/ /  
    |/| | | | | |   
    | * | | | | | 3b944b0	vincentalvo	2014-01-14	Image plugin: old revisions thumbnail error
    |/ / / / / /  
    * | | | | | 8444383	benjaoming	2014-01-12	do not build docs in build-sdist, it's not needed
    * | | | | | bf68a1c	benjaoming	2014-01-12	Fix pluginbase incompatibility with django 1.6 #213
    | |_|_|/ /  
    |/| | | |   
    * | | | | 1bedcb2	Russell-Jones	2014-01-10	Remove six
    * | | | | 4cbedac	Russell-Jones	2014-01-10	travis-ci uses the branch committed to, reverted.
    * | | | | 6433be4	Russell-Jones	2014-01-10	Update requirements_1.6.txt
    * | | | | da8baf6	Russell-Jones	2014-01-10	Update .travis.yml
    * | | | | 53807f5	benjaoming	2014-01-09	add rtd conf env
    * | | | |   ecd2dec	benjaoming	2014-01-09	Merge pull request #227 from spookylukey/easy_branding
    |\ \ \ \ \  
    | |_|_|/ /  
    |/| | | |   
    | * | | | 051ca6e	Luke Plant	2014-01-09	Corrected docs for easy branding method
    | * | | | d1ea57b	Luke Plant	2014-01-09	Added easy way to brand the wiki, avoiding lots of copy and paste.
    | * | | | 3b7420e	Luke Plant	2014-01-09	Beginnings of docs - converted from README
    |/ / / /  
