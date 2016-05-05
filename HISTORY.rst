Latest Changes
==============


Compiled on: Fri May  6 00:30:08 CEST 2016::

    * 61deb6e - (HEAD, master) Changes related to change in lessc (17 seconds ago) <Benjamin Bach>
    * 6054c31 - (origin/master, origin/HEAD) reformat news headlines (4 minutes ago) <Benjamin Bach>
    * 24cd1d8 - Remove irrelevant 0.1 roadmap, add news (6 minutes ago) <Benjamin Bach>
    * 7a53fec - Bump title, add release notes (10 minutes ago) <Benjamin Bach>
    *   adcfdb4 - Merge pull request #544 from benjaoming/testproject-layout (16 minutes ago) <Benjamin Bach>
    |\  
    | * a2792ff - (origin/testproject-layout, testproject-layout) Add custom error pages (22 minutes ago) <Benjamin Bach>
    | * 1cbb688 - add missing context processors in testproject (26 minutes ago) <Benjamin Bach>
    * |   1a37f15 - Merge pull request #543 from benjaoming/testproject-layout (36 minutes ago) <Benjamin Bach>
    |\ \  
    | |/  
    | * 5cf5745 - Clean up thumbnaill db, use en-us as default lang (46 minutes ago) <Benjamin Bach>
    | * 6b999ec - settings.local to use .dev by default (47 minutes ago) <Benjamin Bach>
    | * b1bf300 - New project layout for testproject (47 minutes ago) <Benjamin Bach>
    |/  
    *   286ac7e - Merge pull request #542 from benjaoming/dj19-static (48 minutes ago) <Benjamin Bach>
    |\  
    | * 082a057 - (origin/dj19-static, dj19-static) Use {% static %} instead of deprecated STATIC_URL (53 minutes ago) <Benjamin Bach>
    |/  
    * 63e9332 - translations (2 hours ago) <Benjamin Bach>
    *   3a8aacc - Merge pull request #541 from benjaoming/precommit (6 hours ago) <Benjamin Bach>
    |\  
    | * 5a41d11 - (origin/precommit, precommit) Adding precommit hooks and removing unused imports, fixing pep8 etc (7 hours ago) <Benjamin Bach>
    |/  
    *   1877b7b - Merge pull request #535 from inflrscns/account_settings (8 hours ago) <Benjamin Bach>
    |\  
    | * c620709 - remove unused get_user_model (6 weeks ago) <Olivia K>
    | * c22803b - doesn't show link if account handling is off, wrote a new filter and two tests (6 weeks ago) <Olivia K>
    | *   cb39356 - Merge pull request #3 from benjaoming/patch-1 (7 weeks ago) <inflrscns>
    | |\  
    | | * d298f8e - Don't expose views when account handling is off (8 weeks ago) <Benjamin Bach>
    | |/  
    | * ab7f782 - account settings page (8 weeks ago) <Olivia K>
    * |   6538381 - Merge pull request #540 from benjaoming/readme-fix (7 days ago) <Benjamin Bach>
    |\ \  
    | * | a49ddd0 - (origin/readme-fix, readme-fix) update first lines about 0.1 release (7 days ago) <Benjamin Bach>
    |/ /  
    * |   f4253e9 - Merge pull request #539 from tiregram/patch-1 (7 days ago) <Benjamin Bach>
    |\ \  
    | * | 6380718 - correct (7 days ago) <tiregram>
    |/ /  
    * |   f89690c - Merge pull request #538 from benjaoming/requirements-fix (11 days ago) <Benjamin Bach>
    |\ \  
    | |/  
    |/|   
    | * 276caa1 - Update default requirements when there's no Django yet installed (clean environments) (11 days ago) <Benjamin Bach>
    |/  
    * f3eeecd - un-americanize a title (9 weeks ago) <Benjamin Bach>
    * 7716b8f - update Makefile a bit (9 weeks ago) <Benjamin Bach>
    *   3335cbd - Merge pull request #531 from irvind/login-title-fix (9 weeks ago) <Benjamin Bach>
    |\  
    | * f2d2fab - Fix login page title. (10 weeks ago) <Eugene Obukhov>
    |/  
    * ccb47ea - Use str version for docs (3 months ago) <Benjamin Bach>
    * 6d2a07e - 100% french translations (3 months ago) <Benjamin Bach>
    * 8bec6e1 - Update history to 0.1 release (3 months ago) <Benjamin Bach>
    * a205bc4 - (tag: releases/0.1) version bump to final 0.1 (3 months ago) <Benjamin Bach>
    *   7806854 - Merge pull request #530 from benjaoming/fix-attachment-search (3 months ago) <benjaoming>
    |\  
    | * 80a4334 - add test for attachment search view (3 months ago) <Benjamin Bach>
    | * b6d163c - Fix 'AttachmentSearchView' object has no attribute 'get_form' (3 months ago) <Benjamin Bach>
    |/  
    *   56abf53 - Merge pull request #527 from inflrscns/admin_panel (3 months ago) <benjaoming>
    |\  
    | * a556db1 - added tests and changed some names (3 months ago) <Olivia K>
    | * 44e702d - added trans tags and removed camelCase (4 months ago) <Olivia K>
    | * 964fe32 - basic admin panel for accounts with superuser priveleges (4 months ago) <Olivia K>
    | *   a6ad477 - Merge pull request #2 from django-wiki/master (4 months ago) <inflrscns>
    | |\  
    * | \   4eb42b3 - Merge pull request #528 from benjaoming/typo-and-gitignore (4 months ago) <benjaoming>
    |\ \ \  
    | |_|/  
    |/| |   
    | * | 0b5afd3 - fix typo in notifications settings form, add .cache to gitignore (4 months ago) <Benjamin Bach>
    * | |   c60cd81 - Merge pull request #526 from benjaoming/prerelease-updates (4 months ago) <benjaoming>
    |\ \ \  
    | * | | ba357e4 - remove out-dated sekizai note (4 months ago) <Benjamin Bach>
    | * | | cfb24eb - Update release notes (4 months ago) <Benjamin Bach>
    | * | | 96febfe - more auto-generated stuff (4 months ago) <Benjamin Bach>
    | * | | 0b1c2b6 - Bump to beta (4 months ago) <Benjamin Bach>
    | * | | 0e56a16 - Backwards-incompatible: Use VERSION tuple like django and auto-add git time stamps (4 months ago) <Benjamin Bach>
    | * | | b17ad16 - Consolidate instructions (4 months ago) <Benjamin Bach>
    | * | | 6a7cbf3 - fix broken badge (4 months ago) <Benjamin Bach>
    * | | |   bd67819 - Merge pull request #525 from benjaoming/prerelease-updates (4 months ago) <benjaoming>
    |\ \ \ \  
    | |/ / /  
    | * | | 5a0f57c - remove unref'ed image (4 months ago) <Benjamin Bach>
    * | | |   2e81af7 - Merge pull request #524 from benjaoming/prerelease-updates (4 months ago) <benjaoming>
    |\ \ \ \  
    | |/ / /  
    | * | | c4e858e - Remove unused image and add 1.9 note (4 months ago) <Benjamin Bach>
    * | | |   18d92f0 - Merge pull request #523 from benjaoming/makefile (4 months ago) <benjaoming>
    |\ \ \ \  
    | |/ / /  
    | * | | 133409b - add TODO to docs [ci-skip] (4 months ago) <Benjamin Bach>
    | * | | cc6ab71 - update TODO.rst (4 months ago) <Benjamin Bach>
    | * | | 8d6272c - refactor scripts into Makefile (4 months ago) <Benjamin Bach>
    | * | | 8f9c1de - remove unused refactor script (4 months ago) <Benjamin Bach>
    | * | | 5aa734e - remove pytest from travis conf (4 months ago) <Benjamin Bach>
    | * | | 6a7822d - add pytest dep to tox.ini (4 months ago) <Benjamin Bach>
    | * | | a8eef92 - Add py.test deps (4 months ago) <Benjamin Bach>
    | * | | 0824431 - use py.test (4 months ago) <Benjamin Bach>
    | * | | 59e18a4 - modify rst syntax for history file (4 months ago) <Benjamin Bach>
    | * | | fab9d11 - use HISTORY.rst and include it in docs (4 months ago) <Benjamin Bach>
    | * | | e948c97 - remove the model chart generator, too much bloat (4 months ago) <Benjamin Bach>
    | |/ /  
    * | |   050e34e - Merge pull request #522 from benjaoming/fix-settings-naming (4 months ago) <benjaoming>
    |\ \ \  
    | * | | 5eed23b - Fix syntax err (4 months ago) <Benjamin Bach>
    | * | |   08d0af4 - Merge branch 'patch-1' of https://github.com/steffann/django-wiki into fix-settings-naming (4 months ago) <Benjamin Bach>
    | |\ \ \  
    | | |/ /  
    | |/| |   
    | | * | d2215e9 - Update settings.py (6 months ago) <Sander Steffann>
    * | | |   6339a64 - Merge pull request #519 from inflrscns/confirm-leave-edit-page (4 months ago) <benjaoming>
    |\ \ \ \  
    | * | | | 5a172b2 - Update edit.html (4 months ago) <Olivia K>
    | * | | | dcd601d - Update sidebar.html (4 months ago) <Olivia K>
    | * | | | bf3181b - Update delete.html (4 months ago) <Olivia K>
    | * | | | 205da4c - Update preview_inline.html (4 months ago) <Olivia K>
    | * | | | 0fb5b1a - alert-error is deprecated (4 months ago) <Olivia K>
    | * | | | 5833adc - included field errors (4 months ago) <Olivia K>
    | * | | | deb86cd - alert-error is deprecated (4 months ago) <Olivia K>
    | * | | | 96a907f - Update edit.html (4 months ago) <Olivia K>
    | * | | | 8ac19d8 - confirm leaving the page (4 months ago) <Olivia K>
    | | |_|/  
    | |/| |   
    | * | |   c793308 - Merge pull request #1 from django-wiki/master (4 months ago) <Olivia K>
    | |\ \ \  
    | | |/ /  
    * | | |   4965e7a - Merge pull request #521 from cXhristian/exception-handling (4 months ago) <benjaoming>
    |\ \ \ \  
    | |_|/ /  
    |/| | |   
    | * | | 86cbdee - Undo weird old changes to exception handling (4 months ago) <Christian Duvholt>
    |/ / /  
    * | |   8eea990 - Merge pull request #517 from benjaoming/fix-dj19-migration (4 months ago) <benjaoming>
    |\ \ \  
    | * | | 603cd64 - Add default arguments that Django 1.9 wants explicitly (4 months ago) <Benjamin Bach>
    |/ / /  
    * | |   a1dff7d - Merge pull request #516 from benjaoming/fix-notifications-form (4 months ago) <benjaoming>
    |\ \ \  
    | * | | 60a36c3 - fix another dj 1.9 context 'form' issue (4 months ago) <Benjamin Bach>
    | * | | 04ef7b7 - update danish (4 months ago) <Benjamin Bach>
    | * | | 57c41c5 - update i18n messages (4 months ago) <Benjamin Bach>
    | * | | 8be1031 - syncup with transifex (4 months ago) <Benjamin Bach>
    * | | | 566ceb4 - Update news (4 months ago) <benjaoming>
    * | | |   07bc4ca - Merge pull request #514 from benjaoming/fix-496 (4 months ago) <benjaoming>
    |\ \ \ \  
    | |/ / /  
    |/| | |   
    | * | | 7b75e49 - Fix #496: Clear image floating before heading 1 levels (4 months ago) <Benjamin Bach>
    |/ / /  
    * | |   c4a040a - Merge pull request #513 from benjaoming/fix-428 (4 months ago) <benjaoming>
    |\ \ \  
    | * | | 439699d - Fix #428: Do not call str() (4 months ago) <Benjamin Bach>
    |/ / /  
    * | |   277a916 - Merge pull request #512 from benjaoming/fix-426 (4 months ago) <benjaoming>
    |\ \ \  
    | * | | 433114e - Fix #426: Add article raw id field to url path admin and auto-populate articleforobject (4 months ago) <Benjamin Bach>
    |/ / /  
    * | |   ecbce03 - Merge pull request #511 from benjaoming/fix-444 (4 months ago) <benjaoming>
    |\ \ \  
    | * | | 60127ba - Add reasonable upper bounds to deps, test latest markdown with tox (4 months ago) <Benjamin Bach>
    |/ / /  
    * | |   2ddb57e - Merge pull request #510 from benjaoming/fix-453 (4 months ago) <benjaoming>
    |\ \ \  
    | * | | 1227ce4 - Cleanup after Markdown: Remove <p> tag from surrounding <figure> (4 months ago) <Benjamin Bach>
    |/ / /  
    * | |   515c6c1 - Merge pull request #509 from benjaoming/fix-469 (4 months ago) <benjaoming>
    |\ \ \  
    | * | | 2bf714f - handle ValueError coming from querystring input (4 months ago) <Benjamin Bach>
    |/ / /  
    * | |   4fc7967 - Merge pull request #508 from benjaoming/fix-457 (4 months ago) <benjaoming>
    |\ \ \  
    | * | | a82c671 - Add Django 1.9 to tests and fix errors (4 months ago) <Benjamin Bach>
    |/ / /  
    * | |   dda53a4 - Merge pull request #507 from benjaoming/fix-testprojecturls (4 months ago) <benjaoming>
    |\ \ \  
    | * | | cd9533b - update testproject settings and urls for django 1.9 (4 months ago) <Benjamin Bach>
    * | | |   622b365 - Merge pull request #506 from benjaoming/fix-testprojecturls (4 months ago) <benjaoming>
    |\ \ \ \  
    | |/ / /  
    | * | | 02e7d51 - fix testproject.urls (4 months ago) <Benjamin Bach>
    |/ / /  
    * | |   db3b1fe - Merge pull request #505 from benjaoming/upgrade-requs (4 months ago) <benjaoming>
    |\ \ \  
    | * | | 8aa4d4e - upgrade testproject for dj 1.9, update requirements of tests (4 months ago) <Benjamin Bach>
    * | | |   c6c50dc - Merge pull request #503 from benjaoming/fix-loaddata (4 months ago) <benjaoming>
    |\ \ \ \  
    | |/ / /  
    |/| | |   
    | * | | e9a7445 - also disable signals in notifications plugin when loading fixtures (5 months ago) <Benjamin Bach>
    | * | | 0d84a9c - Refactor all model save() to signals. Add tests. Fixes loaddata issues #501. (5 months ago) <Benjamin Bach>
    |/ / /  
    * | |   525cf62 - Merge pull request #500 from benjaoming/remove-readmerst-auto-conv (5 months ago) <benjaoming>
    |\ \ \  
    | * | | 0421bd7 - remove pypandoc for generating readme.rst, it's already there (5 months ago) <Benjamin Bach>
    * | | |   aa52d19 - Merge pull request #495 from benjaoming/fix-missing-migrations (5 months ago) <benjaoming>
    |\ \ \ \  
    | |/ / /  
    | * | | c5b1c2a - (origin/fix-missing-migrations) Fix migrations #472 and update test database (6 months ago) <Benjamin Bach>
    | | |/  
    | |/|   
    * | |   009fbf2 - Merge pull request #493 from benjaoming/readme-to-rst (6 months ago) <benjaoming>
    |\ \ \  
    | |/ /  
    |/| |   
    | * | 78f4345 - fix link for wikipedia extensions (6 months ago) <Benjamin Bach>
    | * | a7a3731 - add README contents to docs (6 months ago) <Benjamin Bach>
    | * | 6d63056 - finally some news (6 months ago) <Benjamin Bach>
    | * | ee56d7b - Move badges to the top (6 months ago) <Benjamin Bach>
    | * | 27d139b - remove README.md and add pandoc-generated README.rst (6 months ago) <Benjamin Bach>
    |/ /  
    * |   93d7cb1 - Merge pull request #473 from django-wiki/wikilink-basepath (6 months ago) <benjaoming>
    |\ \  
    | * | 4b1a57a - (origin/wikilink-basepath) Use correct base path for [[ article-link ]] syntax (7 months ago) <benjaoming>
    * | |   012d7e5 - Merge pull request #465 from fritz-k/master (6 months ago) <benjaoming>
    |\ \ \  
    | * | | 8eab4a6 - Explicitly default to auth.Group on django <= 1.6 (8 months ago) <Simon Kaiser>
    | * | | 5595dbc - Add tests for WIKI_GROUP_MODEL setting (8 months ago) <Simon Kaiser>
    | * | | 1ffc4a7 - Clarify WIKI_GROUP_MODEL django requirement (8 months ago) <Simon Kaiser>
    | * | | d76cea8 - Add option to use custom Group model with wiki (8 months ago) <Simon Kaiser>
    * | | |   3d2ad05 - Merge pull request #476 from thomastu/validateRevisionTitle (6 months ago) <benjaoming>
    |\ \ \ \  
    | * | | | 62a5b09 - python 3 changes (6 months ago) <Thomas Tu>
    | * | | | d05c17c - clean_title method (6 months ago) <Thomas Tu>
    | * | | | ecdf3e8 - add docstring (6 months ago) <Thomas Tu>
    | * | | | 0863b85 - disallow whitespace only titles (6 months ago) <Thomas Tu>
    | * | | | 9363a42 - raise validation error if missing title (6 months ago) <Thomas Tu>
    * | | | |   fdd0597 - Merge pull request #488 from reduxionist/patch-1 (6 months ago) <benjaoming>
    |\ \ \ \ \  
    | * | | | | 7c04447 - Update README.md (6 months ago) <Jonathan Barratt>
    * | | | | |   78ed399 - Merge pull request #489 from reduxionist/patch-2 (6 months ago) <benjaoming>
    |\ \ \ \ \ \  
    | |/ / / / /  
    |/| | | | |   
    | * | | | | 5e5c95e - Update installation.rst (6 months ago) <Jonathan Barratt>
    |/ / / / /  
    * | | | |   e28776a - Merge pull request #487 from myth/master (6 months ago) <Christian Duvholt>
    |\ \ \ \ \  
    | * | | | | f846614 - Fix a bug introduced in 0e3d363dcdc39167d652bcd1fe44d838df131cef where the function pointers to diff and merge view functions are attached as an instance method on the class instead of a staticmethod. This caused 'self' to be passed as first argument to these views, resulting in stacktraces for these views. (6 months ago) <myth>
    |/ / / / /  
    * | | | | 6748837 - revert replacements made to binary files in 79be863ec3ae4a78351eaf91af110ffb2daa16a0 and remove outdated test dbs (6 months ago) <Benjamin Bach>
    * | | | |   a545bb1 - Merge pull request #478 from guettli/patch-1 (6 months ago) <benjaoming>
    |\ \ \ \ \  
    | * | | | | 3e54d42 - Fixed version info in docs. (6 months ago) <Thomas Güttler>
    * | | | | |   93f6f79 - Merge pull request #479 from guettli/patch-2 (6 months ago) <benjaoming>
    |\ \ \ \ \ \  
    | |/ / / / /  
    |/| | | | |   
    | * | | | | 30607ab - fixed typo in docs for Django1.8 (6 months ago) <Thomas Güttler>
    |/ / / / /  
    * | | | |   6c9520b - Merge pull request #477 from guettli/master (6 months ago) <benjaoming>
    |\ \ \ \ \  
    | * | | | | 79be863 - - replaced: github.com/benjaoming/django-wiki to github.com/django-wiki/django-wiki (6 months ago) <Thomas Guettler>
    |/ / / / /  
    * | | | |   b1fba36 - Merge pull request #474 from spookylukey/fix_deprecation_warnings (7 months ago) <benjaoming>
    |\ \ \ \ \  
    | * | | | | 92a9e88 - Test against latest django-nyt (7 months ago) <Luke Plant>
    | * | | | | 00d623f - Fixed a Django 1.8+ deprecation warning from smartif (7 months ago) <Luke Plant>
    | * | | | | eb9a1dd - Fixed Django 1.8+ deprecation warnings for SimpleTestCase.urls (7 months ago) <Luke Plant>
    | * | | | | 90e9d0f - Fixed Django 1.8+ deprecation warnings for 'TEMPLATES' (7 months ago) <Luke Plant>
    | * | | | | 7c54167 - Fixed Django 1.8+ deprecation warnings for render_to_string (7 months ago) <Luke Plant>
    | * | | | | 0e3d363 - Fixed Django 1.8+ deprecation warning for string view names with url() (7 months ago) <Luke Plant>
    | * | | | | 27a34dc - Fixed Django 1.7+ deprecation warnings for django.utils.importlib (7 months ago) <Luke Plant>
    | * | | | | 5ddc455 - Fixed Django 1.8+ deprecation warnings for get_form form_class argument (7 months ago) <Luke Plant>
    * | | | | |   4622bcd - Merge pull request #471 from spookylukey/mptt_version_fix (7 months ago) <benjaoming>
    |\ \ \ \ \ \  
    | |/ / / / /  
    | | | | / /   
    | |_|_|/ /    
    |/| | | |     
    | * | | | 089229c - Be more cautious about mptt versions (7 months ago) <Luke Plant>
    | * | | | 2732f0f - Allow django-mptt > 0.7.1 as a dependency (7 months ago) <Luke Plant>
    |/ / / /  
    * | | | 859c8d0 - Should depend on django_nyt migrations (7 months ago) <benjaoming>
    * | | | 405f807 - Add note that demo is running the master branch. (8 months ago) <benjaoming>
    | |/ /  
    |/| |   
    * | |   d14e6b8 - Merge pull request #463 from django-wiki/plugin-template-tag (8 months ago) <benjaoming>
    |\ \ \  
    | * | | e6316fd - (origin/plugin-template-tag) a template tag for testing if a plugin is installed (8 months ago) <Benjamin Bach>
    | * | | 82dc282 - fix tests for when pygments is added (8 months ago) <Benjamin Bach>
    | * | | b7a3301 - pep8 and import cleanup (8 months ago) <Benjamin Bach>
    | * | | 66ef2ef - pep8 (8 months ago) <Benjamin Bach>
    |/ / /  
    * | |   3965ae6 - Merge pull request #460 from PolyLAN/fix_error_in_import_script (8 months ago) <benjaoming>
    |\ \ \  
    | * | | 3852f86 - Import all history (8 months ago) <Maximilien Cuony>
    | * | | ea1a5ad - Remove useless u (8 months ago) <Maximilien Cuony>
    | * | | 7d477b3 - Remove useless u (8 months ago) <Maximilien Cuony>
    | * | | b0f1e74 - Fix encoding issues in import (8 months ago) <Maximilien Cuony>
    | * | | 4e13117 - Error in import script (8 months ago) <Maximilien Cuony>
    |/ / /  
    * | | 6070a16 - add note about serving static media #446 (9 months ago) <Benjamin Bach>
    * | | b7e0a72 - dj 1.8 syntax err in example (9 months ago) <Benjamin Bach>
    * | | 671c271 - use rtd theme for local builds (9 months ago) <Benjamin Bach>
    * | | 57c0adf - pep8 (9 months ago) <Benjamin Bach>
    * | | 047233d - use syntax highlighting for python code blocks (9 months ago) <Benjamin Bach>
    * | |   dd13cb4 - Merge pull request #442 from thomastu/attachmentUploadTweak (9 months ago) <benjaoming>
    |\ \ \  
    | * | | 86b3578 - Need to encode test values since b'foo' != 'bar' (10 months ago) <Thomas Tu>
    | * | | c578318 - handle python 3.4 encode behaviour (10 months ago) <Thomas Tu>
    | * | | cea2b37 - Make error message specify filename. (10 months ago) <Thomas Tu>
    | * | | 3125158 - handle ObjectDoesNotExist when using latest() (10 months ago) <Thomas Tu>
    | * | | 7459fd7 - included test for replace with removing previous file as opposed to appending it (10 months ago) <Thomas Tu>
    | * | | 3b079c7 - remove assumption that cleaned_data[replace] existsand nest if statement (10 months ago) <Thomas Tu>
    | * | | b5781a9 - tweak replace behavior (10 months ago) <Thomas Tu>
    | |/ /  
    * | |   ecc70ff - Merge pull request #449 from Russell-Jones/patch-1 (9 months ago) <benjaoming>
    |\ \ \  
    | * | | 579198d - Typo and missing import in installation instructions. (9 months ago) <Russell-Jones>
    | | |/  
    | |/|   
    * | | bf8e69a - Fix #455 replace html input type button with submit (9 months ago) <Benjamin Bach>
    * | |   655c1c3 - Merge pull request #452 from inflrscns/image-markdown-patch (9 months ago) <benjaoming>
    |\ \ \  
    | * | | 25fb770 - Patch for image markdown (9 months ago) <Olivia K.>
    | |/ /  
    * | |   3ccd5cc - Merge pull request #450 from inflrscns/horizontal-scrolling-code (9 months ago) <benjaoming>
    |\ \ \  
    | |/ /  
    |/| |   
    | * | 1437073 - horizontal scrolling on code segments (9 months ago) <Olivia K.>
    | * | 567adb6 - horizontal scrolling on code segments (9 months ago) <Olivia K.>
    |/ /  
    * |   bf21fed - Merge pull request #447 from django-wiki/fix-445 (10 months ago) <benjaoming>
    |\ \  
    | |/  
    |/|   
    | * b28edfe - add sane_lists to settings, fixes #445 (10 months ago) <Benjamin Bach>
    |/  
    *   2370578 - Merge pull request #439 from spookylukey/django_15_fixes (10 months ago) <benjaoming>
    |\  
    | * b585967 - Monkey patch for TreeManager to fix Django 1.8 failures (10 months ago) <Luke Plant>
    | * e53becc - Correct get_query_set compat for Django 1.5 (10 months ago) <Luke Plant>
    | * 62fb928 - Fixed test on Django 1.5 (10 months ago) <Luke Plant>
    | * f8768e0 - Get all tests to run on Django 1.5 (10 months ago) <Luke Plant>
    * |   b10974c - Merge pull request #438 from spookylukey/better_tox_ini (10 months ago) <benjaoming>
    |\ \  
    | |/  
    |/|   
    | * 887b9d2 - Test against most recent Django versions (10 months ago) <Luke Plant>
    | * e9c5d34 - Much more DRY and reabable tox.ini, thanks to new features in tox. (10 months ago) <Luke Plant>
    |/  
    *   9db0d8a - Merge pull request #433 from bargool/master (11 months ago) <benjaoming>
    |\  
    | * dbcf87d - Escape unicode filename while download attachment. Got "embedded newline in response header with name 'Content-Disposition'" Error with Apache (11 months ago) <Alexey Nakoryakov>
    |/  
    *   ef17887 - Merge pull request #431 from cXhristian/article-slug-hyphen (11 months ago) <benjaoming>
    |\  
    | * 68b24d8 - Allow hyphens in article slug. Fixes #391 (11 months ago) <Christian Duvholt>
    |/  
    *   12418be - Merge pull request #429 from csrcordeiro/master (12 months ago) <benjaoming>
    |\  
    | * a21a23e - #418 - Search pagination fix (12 months ago) <César Cordeiro>
    |/  
    *   2efbad6 - Merge pull request #427 from spookylukey/fix_django18_project_compat (12 months ago) <benjaoming>
    |\  
    | * 745c3e4 - Fixed last commit for Django < 1.8 projects (12 months ago) <Luke Plant>
    | * 120c1f7 - Adjust for Django 1.8's handling of TEMPLATES/TEMPLATE_CONTEXT_PROCESSORS in docs/config checks (12 months ago) <Luke Plant>
    |/  
    * b8b1711 - Add docs badge (1 year ago) <benjaoming>
    *   897cf82 - Merge pull request #422 from tkliuxing/doc_disqus (1 year ago) <benjaoming>
    |\  
    | * a8ddbc5 - Add Disqus comment tips to document. (1 year ago) <Ronald Bai>
    |/  
    * 144e70c - Add note about not using Github for support. (1 year ago) <benjaoming>
    * fce1a8e - tox syntax error (1 year ago) <Benjamin Bach>
    * 68a3d73 - add an FAQ to docs [skip-ci] (1 year ago) <Benjamin Bach>
    * 203cb88 - deprecate django.contrib.contenttypes.generic (1 year ago) <Benjamin Bach>
    * 23e164d - bump versions to use django-nyt signed copies (1 year ago) <Benjamin Bach>
    * 8d3ad47 - django 1.9 deprecation (1 year ago) <Benjamin Bach>
    * 332248f - up django_nyt version (1 year ago) <Benjamin Bach>
    * 98b4819 - fix link to dj nyt (1 year ago) <Benjamin Bach>
    * afe4aa0 - clarify notification problem further [skip-ci] (1 year ago) <Benjamin Bach>
    * f21787e - Pull changes from Transifex and recompile (1 year ago) <Benjamin Bach>
    * 2ed962c - Add transifex info (1 year ago) <benjaoming>
    * 029131b - fix syntax errors in Spanish translation and compile (1 year ago) <Benjamin Bach>
    * 5ea252b - transifex configuration (1 year ago) <Benjamin Bach>
    * 8eaab61 - source file main info updated (1 year ago) <Benjamin Bach>
    * 50204c3 - adding english source language [skip-ci] (1 year ago) <Benjamin Bach>
    * 56c8072 - add coverage to the tox environment because otherwise it doesnt pick up data (1 year ago) <Benjamin Bach>
    * d14746a - remove stale and broken import (1 year ago) <Benjamin Bach>
    *   628c23a - Merge pull request #396 from WayneSan/fix_user_model_compatible (1 year ago) <benjaoming>
    |\  
    | * 580d641 - Fixed the compatible with the `USERNAME_FIELD` for the Django version below 1.5. (1 year, 2 months ago) <WayneSan>
    * |   57006d1 - Merge branch 'Alkalit-master' (1 year ago) <Benjamin Bach>
    |\ \  
    | * | 2c15ab4 - Move URL tests to separate test case and use custom urlconf with custom WikiURLPatterns class (1 year ago) <Benjamin Bach>
    | * | b8ce53f - pep8 (1 year ago) <Benjamin Bach>
    | * |   bdb738c - Merge branch 'master' of https://github.com/Alkalit/django-wiki into Alkalit-master (1 year ago) <Benjamin Bach>
    | |\ \  
    |/ / /  
    | * | 7df5d7a - Tests for get_absolute_url with no root url. (1 year, 3 months ago) <Alkalit>
    | * | 9d51c83 - More specific assert (1 year, 3 months ago) <Alkalit>
    | * | 9d64fde - Are few tests for article model. (1 year, 3 months ago) <Alkalit>
    | * | a1bcf0f - Removed redundant user assignment (1 year, 3 months ago) <Alkalit>
    | * | d226dee - Added some explanation. (1 year, 3 months ago) <Alkalit>
    * | |   a229aec - Merge branch 'cXhristian-style-fixes' (1 year ago) <Benjamin Bach>
    |\ \ \  
    | * \ \   881c55e - Merge branch 'style-fixes' of https://github.com/cXhristian/django-wiki into cXhristian-style-fixes (1 year ago) <Benjamin Bach>
    | |\ \ \  
    |/ / / /  
    | * | | cefb595 - Fix small select height caused by .form-control (1 year, 3 months ago) <Christian Duvholt>
    | * | | ff848c8 - Bootstrapify attachment search input (1 year, 3 months ago) <Christian Duvholt>
    | * | | f0d5432 - Improve responsive breaking on article delete button (1 year, 3 months ago) <Christian Duvholt>
    | * | | 037e151 - Less huge buttons (1 year, 3 months ago) <Christian Duvholt>
    | * | | 937fb15 - Moved icons to the left side in accordions (1 year, 3 months ago) <Christian Duvholt>
    | * | | 52a2c7b - Grayed out text on article changes is now more readable and sane (1 year, 3 months ago) <Christian Duvholt>
    | * | | d1576d3 - Improve columns on settings page. Improve look of the add image button (1 year, 3 months ago) <Christian Duvholt>
    | * | | 5933d44 - Add bootstrap class to input field (1 year, 3 months ago) <Christian Duvholt>
    * | | |   b6c022f - Merge branch 'test_tags' of https://github.com/Alkalit/django-wiki into Alkalit-test_tags (1 year ago) <Benjamin Bach>
    |\ \ \ \  
    | * | | | 9c96838 - Hotfix (1 year, 3 months ago) <Alkalit>
    | * | | | 8f79ac2 - assertCountEqual copypasted from SIX module (1 year, 3 months ago) <Alkalit>
    | * | | | b039e19 - TestModel replaced with Article. Used six version of assertCountEqual. (1 year, 3 months ago) <Alkalit>
    | * | | | bd1c92e - Hot fix (forgot add base.py changes) (1 year, 3 months ago) <Alkalit>
    | * | | | 61b8157 - Tests for template tags. (1 year, 3 months ago) <Alkalit>
    | | |/ /  
    | |/| |   
    * | | | 4579f59 - write some release notes and put newest version at the top (1 year ago) <Benjamin Bach>
    * | | | 075d8e7 - Add note on Django 1.8 being supported (1 year ago) <benjaoming>
    * | | | 52cbe2e - hi coverage, now I get how to use -p and combine (1 year ago) <Benjamin Bach>
    * | | | 372c191 - remove coverage combine to resolve why coverage data is no longer collected (1 year ago) <Benjamin Bach>
    * | | | 1aa6a8f - fix test failure on django 1.5, non-relevant for rest of codebase since children.xx is not called anywhere (1 year ago) <Benjamin Bach>
    * | | | 1aac89d - do not hide link to image management when there are no images because they may have been deleted, so should be possible to restore. Also rename replacement button fix #119 (1 year ago) <Benjamin Bach>
    * | | | 91bcd5e - Sort lower levels in [article_list] alphabetically - fix #253 (1 year ago) <Benjamin Bach>
    * | | | 38ae540 - remove headerid from default markdown extensions as it does no good by adding non-unique ids, instead add prefix to [TOC], fix #393 (1 year ago) <Benjamin Bach>
    * | | | d3b0417 - Remove import of removed functions in newer python-markdown fix #406 (1 year ago) <Benjamin Bach>
    * | | | 2c675c7 - rearranging some commit/rollback calls as blocks are atomic, fixes django 1.8 test problems (1 year ago) <Benjamin Bach>
    * | | | 63be843 - remove redundant commits and rollbacks since models.URLPath.create_article is the atomic call (1 year ago) <Benjamin Bach>
    * | | | 8dc0f5c - more occurrences of patterns() being conditionally replaced by a list in django 1.8 (1 year ago) <Benjamin Bach>
    * | | | 66cbb8c - update default links to new repo (1 year ago) <Benjamin Bach>
    * | | | 0467291 - use urlpatterns as list instead of patterns() if django is 1.8+ (1 year ago) <Benjamin Bach>
    * | | | 8e6b374 - use django-sekizai git repo for django 1.8 compat (1 year ago) <Benjamin Bach>
    * | | | d3b16ab - reverse get_queryset vs get_query_set to avoid warnings (1 year ago) <Benjamin Bach>
    * | | | 78b6d46 - set default permanent redirect to false (1 year ago) <Benjamin Bach>
    * | | | 6d35886 - remove loading of url from future (1 year ago) <Benjamin Bach>
    * | | | 9d6eba5 - move coverage argument where it belongs (1 year ago) <Benjamin Bach>
    * | | | 65664e9 - make 'wiki' the source package once again (1 year ago) <Benjamin Bach>
    * | | | a24f2ef - hi travis, please run this now again with my correction (1 year ago) <Benjamin Bach>
    * | | | ace0d62 - Add caching for travis and collect coverage data while running tox (1 year ago) <Benjamin Bach>
    * | | | 2e70090 - do not run tests for every tox, just after all envs are processed (1 year ago) <Benjamin Bach>
    * | | | 8be12ad - add dependency link for current django-sekizai github master branch for django 1.8 (1 year ago) <Benjamin Bach>
    * | | | e7d5e43 - specify python compatibility in setup.py (1 year ago) <Benjamin Bach>
    * | | | ee67810 - modify tox envs to match new 3.4 and 1.8 (1 year ago) <Benjamin Bach>
    * | | | 77c5e46 - do not trust sekizai 0.8 yet (1 year ago) <Benjamin Bach>
    * | | | 561f856 - Do not set _default_manager due to error with django-mptt 0.7+ which is required for django 1.7+ (1 year ago) <Benjamin Bach>
    * | | | e0b0f11 - use GenericIPAddressField if available (1 year ago) <Benjamin Bach>
    * | | | d3c6f19 - Log MPTT error and reraise exception for better traceback (1 year ago) <Benjamin Bach>
    * | | | 3643f7f - should use a real alternative (1 year ago) <Benjamin Bach>
    * | | | 0448709 - Use python 3.4 instead of 3.3 and add django 1.8 (1 year ago) <Benjamin Bach>
    * | | | 2422483 -  Add Python 3 trove classifier (1 year ago) <Benjamin Bach>
    * | | | 6cd1fed - check that django.contrib.sites is installed (1 year ago) <Benjamin Bach>
    * | | | f8933fc - Delete BitDeli, service is down (1 year, 1 month ago) <benjaoming>
    * | | |   f2594c7 - Merge branch 'jdcaballerov-master' (1 year, 2 months ago) <Benjamin Bach>
    |\ \ \ \  
    | * \ \ \   2b44024 - Merge branch 'master' of git://github.com/jdcaballerov/django-wiki into jdcaballerov-master (1 year, 2 months ago) <Benjamin Bach>
    | |\ \ \ \  
    |/ / / / /  
    | * | | | 01860db - Update README.md (1 year, 2 months ago) <jdcaballerov>
    * | | | |   40f1810 - Merge pull request #400 from hwkns/patch-1 (1 year, 2 months ago) <benjaoming>
    |\ \ \ \ \  
    | * | | | | 214818d - import all models to appease Django 1.7 migrations (1 year, 2 months ago) <Daniel Hawkins>
    |/ / / / /  
    * | | | |   db11e26 - Merge pull request #397 from orblivion/patch-4 (1 year, 2 months ago) <benjaoming>
    |\ \ \ \ \  
    | |_|_|_|/  
    |/| | | |   
    | * | | | 97d6957 - Fixes settings.py comment (1 year, 2 months ago) <orblivion>
    |/ / / /  
    * | | |   adb4e2e - Merge pull request #392 from cXhristian/article-menu-responsive (1 year, 3 months ago) <benjaoming>
    |\ \ \ \  
    | |_|_|/  
    |/| | |   
    | * | | 1626481 - Hide article menu labels in mobile view (1 year, 3 months ago) <Christian Duvholt>
    |/ / /  
    * | |   bc5eda5 - Merge pull request #388 from azaghal/issue_387 (1 year, 3 months ago) <benjaoming>
    |\ \ \  
    | * | | 34beb03 - Added additional block to base template that allows overriding the site title (within <title> tag). Implements #387. (1 year, 3 months ago) <Branko Majic>
    |/ / /  
    * | |   670a2f5 - Merge pull request #386 from Alkalit/master (1 year, 3 months ago) <benjaoming>
    |\ \ \  
    | | |/  
    | |/|   
    | * | b146c62 - Added better doc's (1 year, 3 months ago) <Alkalit>
    | * | c2712e6 - Filters code refactoring. Also added some docs. (1 year, 3 months ago) <Alkalit>
    * | |   9b8be37 - Merge pull request #382 from Alkalit/master (1 year, 3 months ago) <benjaoming>
    |\ \ \  
    | |/ /  
    | * | c43c971 - Tests for get_content_snippet filter. (1 year, 3 months ago) <Alkalit>
    | * | 211df32 - Mock library removed as requirement. (1 year, 3 months ago) <Alkalit>
    | * | 03ac42a - mock replaced by custom override decorator. (1 year, 3 months ago) <Alkalit>
    | * | 43ac168 - Mock library added as requirements (1 year, 3 months ago) <Alkalit>
    | * | 0f0b486 - Tests for template filters. (1 year, 3 months ago) <Alkalit>
    * | | f89f169 - Force test images to be part of testproject data (1 year, 3 months ago) <Benjamin Bach>
    * | | 4c31006 - move badges below PyPi ignore seperator (1 year, 3 months ago) <Benjamin Bach>
    * | | 2044c41 - Merge pull request #384 from cXhristian/releases/0.0.24 (1 year, 3 months ago) <benjaoming>
    * | | 6daab12 - reference release notes in upgrade instructions (1 year, 3 months ago) <Benjamin Bach>
    * | | c2816c4 - instructions for upgrading added to release notes (1 year, 3 months ago) <Benjamin Bach>
    * | |   e22af9e - Merge pull request #380 from Alkalit/master (1 year, 3 months ago) <benjaoming>
    |\ \ \  
    | |/ /  
    | * | 6a6751c - view tests refactoring. (1 year, 3 months ago) <Alkalit>
    * | |   9237dee - Merge pull request #379 from Alkalit/master (1 year, 3 months ago) <benjaoming>
    |\ \ \  
    | |/ /  
    | * | bbc118a - Tests for managers moved into separate file. Test cases also separated into classes and methods. (1 year, 3 months ago) <Alkalit>
    | * | 6def369 - Are few obvious fixes. (1 year, 3 months ago) <Alkalit>
    | * | 3640d36 - Unit tests: pep8 refactoring and some prettification. (1 year, 3 months ago) <Alkalit>
    |/ /  
    * |   18f01b3 - Merge pull request #378 from cXhristian/django-1.7-mimetype (1 year, 3 months ago) <benjaoming>
    |\ \  
    | * | f396871 - Use content_type instead of mimetype. Mimetype was removed in Django 1.7 (1 year, 3 months ago) <Christian Duvholt>
    |/ /  
    * | 89145e8 - Re add empty module due to import errors in later life (1 year, 3 months ago) <Benjamin Bach>
    * | b30609d - Revert errornous change by autopep8 (1 year, 3 months ago) <Benjamin Bach>
    * | fe60614 - pep8 various files outside of wiki package #287 (1 year, 3 months ago) <Benjamin Bach>
    * | 7620d13 - move bitdeli, not that pep8 is fixed (1 year, 3 months ago) <Benjamin Bach>
    * |   0d16237 - Merge pull request #376 from bitdeli-chef/master (1 year, 3 months ago) <benjaoming>
    |\ \  
    | * | 703256e - Add a Bitdeli badge to README (1 year, 3 months ago) <Bitdeli Chef>
    |/ /  
    * | 762a808 - WARNING! autopep8 on whole codebase - fix #287 (1 year, 3 months ago) <Benjamin Bach>
    * | 2abb051 - trying out task list (1 year, 3 months ago) <Benjamin Bach>
    * | a3bd1b4 - image revision table incorrectly named (1 year, 3 months ago) <Benjamin Bach>
    * | 778cabe - image revision table incorrectly named (1 year, 3 months ago) <Benjamin Bach>
    * | e4ba2d9 - version bump to 0.1 (1 year, 3 months ago) <Benjamin Bach>
    * | 93744c3 - add credit where due! (1 year, 3 months ago) <Benjamin Bach>
    * | 93ffee4 - Reset migrations and delete ghost migrations on test db (1 year, 3 months ago) <Benjamin Bach>
    * |   56b055a - Merge branch 'spookylukey-fix_django_17' (1 year, 3 months ago) <Benjamin Bach>
    |\ \  
    | * \   b860286 - Merge branch 'fix_django_17' of https://github.com/spookylukey/django-wiki into spookylukey-fix_django_17 (1 year, 3 months ago) <Benjamin Bach>
    | |\ \  
    | | * | 5366066 - Made tox.ini more DRY (1 year, 4 months ago) <Luke Plant>
    | | * | 9c4bbb4 - Fixed error in docs (1 year, 4 months ago) <Luke Plant>
    | | * | b8bd6f2 - Added initial Django 1.7 migrations (1 year, 4 months ago) <Luke Plant>
    | | * | dfd6577 - Corrected silly error in tox.ini (1 year, 4 months ago) <Luke Plant>
    | | * | 0487e9b - Fixed Django 1.7 support (1 year, 5 months ago) <Luke Plant>
    | | * | 5cbc2d3 - Fixed deprecation warnings on Django >= 1.6 due to get_query_set (1 year, 5 months ago) <Luke Plant>
    | | * | ea5373d - Removed need for SOUTH_MIGRATION_MODULES by requiring South >= 1.0 (1 year, 5 months ago) <Luke Plant>
    * | | | 577bfe8 - update tox for latest django nyt (1 year, 3 months ago) <Benjamin Bach>
    * | | | f48a644 - Remove unused Travis requirements (1 year, 3 months ago) <Benjamin Bach>
    * | | | c773844 - Update Django requirements (1 year, 3 months ago) <Benjamin Bach>
    * | | |   78ec5b1 - Merge branch 'django1.7' (1 year, 3 months ago) <Benjamin Bach>
    |\ \ \ \  
    | * | | | 65f72f5 - fix wrongly resetting notification badge color at every update (1 year, 9 months ago) <benjaoming>
    | * | | | 4d5b2f1 - Merge pull request #269 from fangsterr/master (1 year, 10 months ago) <benjaoming>
    | * | | | c2a8e8e - Fix #270 (1 year, 10 months ago) <benjaoming>
    | * | | |   5c7f7a7 - Merge commit 'efae942cc3613364e960fcc8da8b48454434ad1e' into django1.7 (1 year, 10 months ago) <benjaoming>
    | |\ \ \ \  
    | * | | | | 85e9ecf - Move to python3-style unicode everywhere str() (1 year, 10 months ago) <Russell Jones>
    | * | | | | 7d5d44b - fix django 1.7 issues related to #255 (2 years, 1 month ago) <benjaoming>
    | * | | | | 1f65079 - fix django 1.7 issues related to #255 (2 years, 1 month ago) <benjaoming>
    * | | | | | bb39fc3 - improve release note compatibility section [skip ci] (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | 32eb8a0 - Removing python 2.5 support notice, it is not longer supported [skip ci] (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | abe31a1 - coveralls badge (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | bc68044 - wheel configuration (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | ad2f48b - tox should test South 1.0.2 since its now the default match for reqs (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | 02d26a8 - trying to fix 'No file to run: 'python'' from invalid example code (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | f0041be - allow for setup.py test to run tests (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | 34a9e65 - update section about requirements (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | a29b0a1 - correcting example data (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | d8fe7d3 - syntax err in travis (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | e936d44 - dependency badge (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | 2c88cf1 - bitdeli (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | 765c7f8 - coveralls test (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | 15b5326 - (tag: alpha/0.0.24) update readme with news on 0.0.24 (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | 220fbb1 - update release notes to reflect fixes in notifications migrations (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | 2ea1242 - add changelog for 0.0.24 (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | 67e9d40 - version bump to 0.0.24 (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | 0dd77b8 - 0.0.24 migrations applied to test database (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | 228cb96 - Do not have MANIFEST.in as a symlink, does not work in distributed zip archives (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | 28561ea - make new table renaming migrations python3 compatible #290 (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | 311f7ce - Output end result when creating articles and make py3 ready (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | 11cc61e - Rename the migration that restores the table in case its already marked as run (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | c232ada - Rename notifications_... tables to wiki_notifications_... #290 (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | 28c55a4 - Remove unused models module (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | bec089b - Rename attachments_... tables to wiki_attachments_... #290 (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | ff14161 - change table names on images plugin #290 (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | 896a133 - conditionally create the articlenotifications table if it doesnt exist because of the old broken migration (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | d248b9d - add empty migration in place of old broken migration from 0.23 (1 year, 3 months ago) <Benjamin Bach>
    * | | | | | 70e295d - note on markdown 2.3 (1 year, 3 months ago) <Benjamin Bach>
    * | | | | |   1cdf0b4 - Merge pull request #372 from Alkalit/master (1 year, 3 months ago) <benjaoming>
    |\ \ \ \ \ \  
    | * | | | | | 1689f3b - future import moved to file top. (1 year, 3 months ago) <Alkalit>
    |/ / / / / /  
    * | | | | |   ffe4b81 - Upgrading to newest bootstrap and font awesome - thanks @cXhristian!! (1 year, 4 months ago) <Benjamin Bach>
    |\ \ \ \ \ \  
    | * | | | | | f053c15 - Add horizontal scrolling to big diffs. Fixed accordion heading CSS. (1 year, 4 months ago) <Christian Duvholt>
    | * | | | | | 515b6cd - Fix history diff collapse (1 year, 4 months ago) <Christian Duvholt>
    | * | | | | | 1e79e72 - Fix navbar collapse (1 year, 4 months ago) <Christian Duvholt>
    | * | | | | | 255c52c - Fix vertical align on typeahead input group (1 year, 4 months ago) <Christian Duvholt>
    | * | | | | | 2e4d49c - Upgrade to Font Awesome 4 (1 year, 4 months ago) <Christian Duvholt>
    | * | | | | | 271431b - Update templates for Bootstrap 3.3.1. Fix modals and search. (1 year, 4 months ago) <Christian Duvholt>
    | * | | | | | b3ccbdd - Upgraded Bootstrap files to 3.3.1 (1 year, 4 months ago) <Christian Duvholt>
    * | | | | | |   3561b2a - Merge pull request #357 from cXhristian/preview-markdown (1 year, 4 months ago) <benjaoming>
    |\ \ \ \ \ \ \  
    | * | | | | | | 4ff8baf - Created a new core markdown extension folder. Moved preview links extension. (1 year, 5 months ago) <Christian Duvholt>
    | * | | | | | | 29d0013 - Set <a target="_blank"> for all links when in preview mode. Fixes #256. (1 year, 5 months ago) <Christian Duvholt>
    * | | | | | | |   7b87e84 - Merge pull request #367 from orblivion/patch-3 (1 year, 4 months ago) <benjaoming>
    |\ \ \ \ \ \ \ \  
    | |_|/ / / / / /  
    |/| | | | | | |   
    | * | | | | | | 12920af - Properly sets default configs in plugins/links/mdx (1 year, 4 months ago) <orblivion>
    |/ / / / / / /  
    * | | | | | | 9a08694 - new demo site url (1 year, 4 months ago) <Benjamin Bach>
    * | | | | | | e9332ca - rtfd badge (1 year, 4 months ago) <Benjamin Bach>
    * | | | | | | b3affd7 - build LESS files for fix of input type=email (1 year, 4 months ago) <Benjamin Bach>
    * | | | | | | 18c2f12 - fix migrations in testproject database (1 year, 4 months ago) <Benjamin Bach>
    * | | | | | | 1de0f20 - Better guidance for upgrading and notifications issue #288 (1 year, 4 months ago) <Benjamin Bach>
    * | | | | | | 1965d0a - Fix up creating default subscriptions, realted to #288 (1 year, 4 months ago) <Benjamin Bach>
    * | | | | | | 117727a - warn about not having changed to django_nyt (1 year, 4 months ago) <Benjamin Bach>
    * | | | | | | c8961f3 - typo and code format (1 year, 4 months ago) <Benjamin Bach>
    * | | | | | | c7ebf2f - Add input[type=email] - fixes #363 (1 year, 4 months ago) <Benjamin Bach>
    * | | | | | | 8f2ef2b - Make Bootstrap/LESS customization easier by putting all custom wiki styles in their own LESS file and not mingle them with the Bootstrap import statement - fixes #364 (1 year, 4 months ago) <Benjamin Bach>
    | |_|_|/ / /  
    |/| | | | |   
    * | | | | |   9976b29 - Merge pull request #360 from orblivion/patch-1 (1 year, 5 months ago) <benjaoming>
    |\ \ \ \ \ \  
    | * | | | | | 9c14f86 - tips.rst - typeo (1 year, 5 months ago) <orblivion>
    |/ / / / / /  
    * | | | | | 2fee7db - cannot concatenate a tuple (1 year, 5 months ago) <benjaoming>
    * | | | | |   24764e3 - Merge pull request #358 from spookylukey/synchronise_travis_and_tox_2 (1 year, 5 months ago) <benjaoming>
    |\ \ \ \ \ \  
    | | |_|_|/ /  
    | |/| | | |   
    | * | | | | 52cba45 - Properly synchronised tox and travis test config (1 year, 5 months ago) <Luke Plant>
    |/ / / / /  
    * | | | |   b8fae91 - Merge pull request #353 from spookylukey/fix_module_name_deprecation (1 year, 5 months ago) <benjaoming>
    |\ \ \ \ \  
    | |/ / / /  
    |/| | | |   
    | * | | | c8ec345 - Fixed dependencies in tox.ini so that tests run (1 year, 5 months ago) <Luke Plant>
    | * | | | 5cb503d - Fixed deprecation warnings issues by migrations. (1 year, 5 months ago) <Luke Plant>
    |/ / / /  
    * | | |   40b0e5d - Merge pull request #352 from cXhristian/notifications-subscription-fix (1 year, 5 months ago) <benjaoming>
    |\ \ \ \  
    | * | | | e3e00ec - Fix #265 (1 year, 5 months ago) <Christian Duvholt>
    |/ / / /  
    * | | |   843225c - Merge pull request #351 from cXhristian/plugins-unicode (1 year, 6 months ago) <benjaoming>
    |\ \ \ \  
    | * | | | 6e4f957 - Add use __str__ with python_2_unicode_compatible for plugins too (1 year, 6 months ago) <Christian Duvholt>
    |/ / / /  
    * | | |   ab8bf24 - Merge pull request #349 from django-wiki/revert-347-plugins-unicode (1 year, 6 months ago) <benjaoming>
    |\ \ \ \  
    | * | | | fd9bb87 - Revert "Add use __str__ with python_2_unicode_compatible for plugins too" (1 year, 6 months ago) <benjaoming>
    |/ / / /  
    * | | |   588e693 - Merge pull request #347 from cXhristian/plugins-unicode (1 year, 6 months ago) <benjaoming>
    |\ \ \ \  
    | * | | | bb3b337 - Add use __str__ with python_2_unicode_compatible for plugins too (1 year, 6 months ago) <Christian Duvholt>
    |/ / / /  
    * | | |   0d012c7 - Merge pull request #346 from jandebleser/master (1 year, 6 months ago) <benjaoming>
    |\ \ \ \  
    | * | | | 87f964a - Fixed problem with cleaning the username when the application is using a custom username field. (1 year, 6 months ago) <Jan De Bleser>
    |/ / / /  
    * | | |   e9495a8 - Merge pull request #345 from cXhristian/attachment-fixes (1 year, 6 months ago) <benjaoming>
    |\ \ \ \  
    | * | | | b46ced1 - Better messages when adding attachments (1 year, 6 months ago) <Christian Duvholt>
    | * | | | 5f58fdf - Clear cache for article when doing something with attachments (1 year, 6 months ago) <Christian Duvholt>
    | * | | | 25e8a47 - Fix many issues with attachments caused by attachment-filter not being specifc enough (1 year, 6 months ago) <Christian Duvholt>
    | * | | | 16a6894 - Fix not being able to add existing attachments to an article (1 year, 6 months ago) <Christian Duvholt>
    | * | | | f8eb556 - Fix broken markdown output when attachment does not exist (1 year, 6 months ago) <Christian Duvholt>
    |/ / / /  
    * | | |   c7f8ff0 - Merge pull request #343 from cXhristian/settings-subscriptions-count (1 year, 6 months ago) <benjaoming>
    |\ \ \ \  
    | * | | | abd304b - Fix notification error in settings (1 year, 6 months ago) <Christian Duvholt>
    |/ / / /  
    * | | | 579c67e - Adding python_2_unicode_compatible from @fsx999, #Fix 282 and Close #342 (1 year, 6 months ago) <paul>
    * | | | 62d67c0 - Fix #341 (1 year, 6 months ago) <benjaoming>
    * | | | c551a69 - Fix #263 and style article list header (1 year, 6 months ago) <benjaoming>
    * | | | 93464ba - add more tests of custom managers and add support for django 1.5 and 1.6's patterns for empty querysets (1 year, 6 months ago) <benjaoming>
    * | | | 294839e - use gettext_lazy where appropriate, thanks @jluttine for starting work on this (1 year, 6 months ago) <benjaoming>
    * | | |   fa01cfb - Merge pull request #337 from fsx999/master (1 year, 6 months ago) <benjaoming>
    |\ \ \ \  
    | * | | | e56a78a - python_2_unicode_compatible decorateur (1 year, 6 months ago) <paul>
    * | | | | 97b4a32 - add tests of none() and empty queryset functionality (1 year, 6 months ago) <benjaoming>
    * | | | | 71f2693 - do not call get_empty_query_set, that's deprecated (1 year, 6 months ago) <benjaoming>
    * | | | | d11a036 - initial tests for custom queryset methods (1 year, 6 months ago) <benjaoming>
    * | | | | f2c2d4d - ignore wiki/attachments for now as it occurs from running tests and should not be distributed (1 year, 6 months ago) <benjaoming>
    * | | | | 7a47924 - pep8 (1 year, 6 months ago) <benjaoming>
    * | | | |   6a76e16 - Merge pull request #338 from cXhristian/future-import-fix (1 year, 6 months ago) <benjaoming>
    |\ \ \ \ \  
    | |/ / / /  
    |/| | | |   
    | * | | | bfcda5f - Move future import to the top (1 year, 6 months ago) <Christian Duvholt>
    |/ / / /  
    * | | |   0d10395 - Merge branch 'kilrogg-master' PR#309 (1 year, 6 months ago) <benjaoming>
    |\ \ \ \  
    | * \ \ \   7bb4334 - Merge branch 'master' of github.com:kilrogg/django-wiki into kilrogg-master (1 year, 6 months ago) <benjaoming>
    | |\ \ \ \  
    | | * | | | aded511 - % fix haystack search query (request.group not set and should be list of all groups) (1 year, 7 months ago) <Benjamin Richter>
    | | * | | | bddeb12 - % fix saving of notification settings (1 year, 7 months ago) <Benjamin Richter>
    | | * | | | 7010312 - % fix notifications overview (1 year, 7 months ago) <Benjamin Richter>
    * | | | | |   93049a3 - Merge pull request #325 from jluttine/fix-testproject-manage (1 year, 6 months ago) <benjaoming>
    |\ \ \ \ \ \  
    | * | | | | | 3d70212 - Fix testproject/manage.py to be executable (1 year, 6 months ago) <Jaakko Luttinen>
    * | | | | | |   60bf09e - Merge pull request #327 from jluttine/fix-326-search-title (1 year, 6 months ago) <benjaoming>
    |\ \ \ \ \ \ \  
    | |_|/ / / / /  
    |/| | | | | |   
    | * | | | | | f83effc - Fix issue #326 (1 year, 6 months ago) <Jaakko Luttinen>
    | |/ / / / /  
    * | | | | | f100e69 - Remove Python 3.2 testing because South migrations arent running (1 year, 6 months ago) <benjaoming>
    * | | | | |   99c8d6b - Merge pull request #330 from spookylukey/reset_notifications_migrations (1 year, 6 months ago) <benjaoming>
    |\ \ \ \ \ \  
    | * | | | | | 38c0007 - Migrations reset on the rather messed up notifications app (1 year, 6 months ago) <Luke Plant>
    * | | | | | | cf96c61 - add note on master branch (1 year, 6 months ago) <benjaoming>
    * | | | | | |   7087775 - Merge pull request #332 from spookylukey/fix_upload_for_python3_rebased (1 year, 6 months ago) <benjaoming>
    |\ \ \ \ \ \ \  
    | * | | | | | | 197bd20 - Fixed uploading of attachments using Python3 (1 year, 6 months ago) <Luke Plant>
    | * | | | | | | 61ffee0 - Removed stray debugging print statement (1 year, 6 months ago) <Luke Plant>
    | * | | | | | | c1b2408 - Fixed bug with caching that was causing a test to fail. (1 year, 6 months ago) <Luke Plant>
    | * | | | | | | 844bbd4 - Pulled out some useful base classes for test cases (1 year, 6 months ago) <Luke Plant>
    | * | | | | | | 13502c6 - Get tests to run under Django 1.4 and 1.5, but without duplication on 1.6 and later (1 year, 6 months ago) <Luke Plant>
    | * | | | | | | 57df9c4 - Updated dependencies in tox.ini to latest supported versions of Django (1 year, 6 months ago) <Luke Plant>
    | * | | | | | | 8145c45 - Tests should be run against current version of django-wiki, not old version! (1 year, 6 months ago) <Luke Plant>
    | | |/ / / / /  
    | |/| | | | |   
    * | | | | | |   1d5c033 - Merge pull request #331 from spookylukey/fix_hashbangs (1 year, 6 months ago) <benjaoming>
    |\ \ \ \ \ \ \  
    | |/ / / / / /  
    |/| | | | | |   
    | * | | | | | f77220e - Fixed runtests.py and setup.py hashbang lines, broken by commit with python-modernizer (1 year, 6 months ago) <Luke Plant>
    |/ / / / / /  
    * | | | | | c91061a - Fix #295 (1 year, 6 months ago) <benjaoming>
    |/ / / / /  
    * | | | | 4549941 - use python-modernizer to fix migrations and other small issues (1 year, 6 months ago) <benjaoming>
    * | | | | 43ce281 - Update travis config, remove django 1.4 stuff (1 year, 6 months ago) <benjaoming>
    * | | | | bc7464d - initial work on danish translation (1 year, 6 months ago) <benjaoming>
    * | | | | 2974f00 - update django-nyt requirement because of python3 (1 year, 6 months ago) <benjaoming>
    * | | | | da57263 - python3 compat bug (1 year, 6 months ago) <benjaoming>
    * | | | | 1574c00 - remove django 1.7 from 0.0.24 travis tests (1 year, 6 months ago) <benjaoming>
    * | | | |   35c7496 - Merge pull request #322 from jluttine/finnish-translation (1 year, 6 months ago) <benjaoming>
    |\ \ \ \ \  
    | * | | | | 90e8443 - Preliminary Finnish translation (1 year, 6 months ago) <Jaakko Luttinen>
    * | | | | |   2e8d918 - Merge pull request #321 from jluttine/fix-requirements (1 year, 6 months ago) <benjaoming>
    |\ \ \ \ \ \  
    | |/ / / / /  
    |/| | | | |   
    | * | | | |   70e78eb - Merge pull request #1 from django-wiki/jluttine-fix-requirements (1 year, 6 months ago) <Jaakko Luttinen>
    | |\ \ \ \ \  
    | | * | | | | bfe7544 - add traceback to reveal why errors in the testing framework occurs (1 year, 6 months ago) <benjaoming>
    | |/ / / / /  
    | * | | | | 8e4cce9 - Fix Django v1.7 in Travis file (1 year, 6 months ago) <Jaakko Luttinen>
    | * | | | | 5a97d1a - Remove a debugging message that was left accidentally (1 year, 6 months ago) <Jaakko Luttinen>
    | * | | | | 17a6890 - Fix South requirement to >=0.8.4 (1 year, 6 months ago) <Jaakko Luttinen>
    | * | | | | 67f7ae9 - Refactor dependencies in requirements.txt and setup.py (1 year, 6 months ago) <Jaakko Luttinen>
    | * | | | | 9e0c9a7 - Fix South handling in requirements (1 year, 6 months ago) <Jaakko Luttinen>
    | * | | | | 7f20035 - Fix Python 2.6 error caused by Markdown updates (1 year, 6 months ago) <Jaakko Luttinen>
    | * | | | | ae85033 - Share common requirements for Travis and distribution (fix #319) (1 year, 6 months ago) <Jaakko Luttinen>
    |/ / / / /  
    * | | | |   55eb10a - Merge pull request #317 from jluttine/fix-travis-mptt (1 year, 6 months ago) <benjaoming>
    |\ \ \ \ \  
    | * | | | | 181435c - Fix Travis CI requirements to use django-mptt==0.6.0 (1 year, 6 months ago) <Jaakko Luttinen>
    |/ / / / /  
    * | | | |   f380852 - Merge pull request #316 from jluttine/fix-travis-url (1 year, 6 months ago) <benjaoming>
    |\ \ \ \ \  
    | * | | | | 84c07fb - Fix Travis-CI URL in README (1 year, 6 months ago) <Jaakko Luttinen>
    |/ / / / /  
    * | | | |   d88db48 - Merge pull request #315 from norkans7/small_fix (1 year, 6 months ago) <benjaoming>
    |\ \ \ \ \  
    | * | | | | 81a3273 - fix css class name (1 year, 6 months ago) <Norbert Kwizera>
    * | | | | |   3754835 - Merge pull request #314 from jluttine/master (1 year, 6 months ago) <benjaoming>
    |\ \ \ \ \ \  
    | |/ / / / /  
    |/| | | | |   
    | * | | | | 9d411a7 - Change empty markdown config to {} instead of None (1 year, 6 months ago) <Jaakko Luttinen>
    |/ / / / /  
    * | | | |   cff1f74 - Merge pull request #313 from jandebleser/master (1 year, 7 months ago) <benjaoming>
    |\ \ \ \ \  
    | * | | | | 43d94e6 - Fixed problem with auth.user in the south migrations for plugin 'images'. (1 year, 7 months ago) <Jan De Bleser>
    |/ / / / /  
    * | | | |   c007ca9 - Merge pull request #312 from jandebleser/master (1 year, 7 months ago) <benjaoming>
    |\ \ \ \ \  
    | |/ / / /  
    |/| | | |   
    | * | | | c618f57 - Fixed problem with auth.user in the south migrations. Further continuation of e506c0941bfed1104394ffc176484c928685080f. (1 year, 7 months ago) <Jan De Bleser>
    |/ / / /  
    * | | |   ffe9c87 - Merge pull request #307 from spookylukey/master (1 year, 7 months ago) <benjaoming>
    |\ \ \ \  
    | * | | | 4ec26b2 - Python 3 compatibility (or at least correct syntax) for mediawikimport command (1 year, 7 months ago) <Luke Plant>
    |/ / / /  
    * | | |   7c10ab9 - Merge pull request #303 from thanhleviet/patch-1 (1 year, 8 months ago) <benjaoming>
    |\ \ \ \  
    | * | | | 5913634 - Update installation.rst (1 year, 8 months ago) <Thanh Lê>
    |/ / / /  
    * | | |   da653dc - Merge pull request #301 from Fantomas42/patch-1 (1 year, 8 months ago) <benjaoming>
    |\ \ \ \  
    | * | | | 036311f - Update .travis.yml (1 year, 8 months ago) <Julien Fache>
    |/ / / /  
    * | | |   16063db - Merge pull request #300 from pknowles/master (1 year, 8 months ago) <benjaoming>
    |\ \ \ \  
    | * | | | 20041bd - Updated setting name ALLOW_OVERLAPPING_THIRD_PARTY_URL to CHECK_SLUG_URL_AVAILABLE (1 year, 8 months ago) <pknowles>
    | * | | | 9eae449 - Added validation for slugs conflicting with 3rd party URLs, and option to disable with ALLOW_OVERLAPPING_THIRD_PARTY_URL = True (1 year, 8 months ago) <pknowles>
    |/ / / /  
    * | | |   20748ad - Merge pull request #299 from tkliuxing/master (1 year, 8 months ago) <benjaoming>
    |\ \ \ \  
    | * | | | a50a5cf - Add Simplified Chinese translation. (1 year, 8 months ago) <Ronald Bai>
    |/ / / /  
    * | | | d0a83ce - Updating model chart. Command used: (1 year, 8 months ago) <benjaoming>
    * | | | b759c5b - give at least anon ready access to front page (1 year, 9 months ago) <benjaoming>
    * | | | 64636dc - update test database and make front page only editable by admin (1 year, 9 months ago) <benjaoming>
    * | | | 74871db - Add a bit more info, and thanks @almereyda for noticing. (1 year, 9 months ago) <benjaoming>
    * | | | bccd5b6 - Add IRC notifications (1 year, 9 months ago) <benjaoming>
    * | | |   4c3d557 - Merge pull request #293 from clincher/patch-1 (1 year, 9 months ago) <benjaoming>
    |\ \ \ \  
    | * | | | e5fbd6b - Update markdown_extensions.py (1 year, 9 months ago) <Василий>
    |/ / / /  
    * | | | ba21cc0 - increase django-nyt version dep (1 year, 9 months ago) <benjaoming>
    * | | | aec9c1e - fix wrongly resetting notification badge color at every update (1 year, 9 months ago) <benjaoming>
    * | | | 25ee8b7 - Add missing migration for deleted field Image.image - Fixes #281 (1 year, 10 months ago) <benjaoming>
    * | | | 1ce1928 - docs change on how to handle notifications for 0.0.24 (1 year, 10 months ago) <benjaoming>
    * | | | 5dd9a98 - dependency on new django_nyt (1 year, 10 months ago) <benjaoming>
    * | | | eea0c43 - notifications plugin form to use django-nyt and management command to recreate notifications (1 year, 10 months ago) <benjaoming>
    * | | |   6f13af4 - Merge pull request #289 from django-wiki/revert-272-fix_224 (1 year, 10 months ago) <benjaoming>
    |\ \ \ \  
    | * | | | 84f7508 - (origin/revert-272-fix_224) Revert "Fix #224" (1 year, 10 months ago) <benjaoming>
    |/ / / /  
    * | | | 1ec4e74 - do not install django-mptt 0.6.1 it's broken (1 year, 10 months ago) <benjaoming>
    * | | | 178aa26 - more info on new releases (1 year, 10 months ago) <benjaoming>
    * | | | eac7504 - Fix #270 (1 year, 10 months ago) <benjaoming>
    * | | |   25f2cd5 - Merge pull request #279 from SacNaturalFoods/update-help-plugin (1 year, 10 months ago) <benjaoming>
    |\ \ \ \  
    | * | | | d404a15 - corrected lists section of help plugin for sub items (1 year, 10 months ago) <tschmidt>
    * | | | | 1614eb5 - add missing paragraph (1 year, 10 months ago) <benjaoming>
    * | | | | 9ff1ab9 - add note about django-wiki-project-template (1 year, 10 months ago) <benjaoming>
    * | | | | a7acc42 - pep8 (1 year, 10 months ago) <benjaoming>
    * | | | |   bacba8d - Merge pull request #269 from fangsterr/master (1 year, 10 months ago) <benjaoming>
    |\ \ \ \ \  
    | * | | | | 5521c3b - article settings form compatibility with custom user model (1 year, 11 months ago) <Andy Fang>
    * | | | | |   8a7f288 - Merge pull request #278 from PolyLAN/fix_262 (1 year, 10 months ago) <benjaoming>
    |\ \ \ \ \ \  
    | * | | | | | 1445ad5 - Fix #262 for attachements (1 year, 10 months ago) <Maximilien Cuony>
    | |/ / / / /  
    * | | | | |   9100c42 - Merge pull request #272 from PolyLAN/fix_224 (1 year, 10 months ago) <benjaoming>
    |\ \ \ \ \ \  
    | * | | | | | 4e7031d - Also fix in the plugin (1 year, 11 months ago) <Maximilien Cuony>
    | * | | | | | fdb6ba8 - Typo, nty->nyt (1 year, 11 months ago) <Maximilien Cuony>
    | * | | | | | 8646f11 - Rename notify to nyt (https://github.com/benjaoming/django-wiki/issues/224#issuecomment-44047813= (1 year, 11 months ago) <Maximilien Cuony>
    | |/ / / / /  
    * | | | | |   daf13cf - Merge pull request #273 from PolyLAN/fix_haystack_confict (1 year, 10 months ago) <benjaoming>
    |\ \ \ \ \ \  
    | * | | | | | 5754e97 - Test the presence of the plugin haystack, not haystack himself (1 year, 11 months ago) <Maximilien Cuony>
    | |/ / / / /  
    * | | | | |   d0e77d0 - Merge pull request #275 from PolyLAN/mediawiki_import (1 year, 10 months ago) <benjaoming>
    |\ \ \ \ \ \  
    | |/ / / / /  
    |/| | | | |   
    | * | | | | 9c5e6b0 - Better import: Expend templates, better url handeling and internal links (1 year, 10 months ago) <Maximilien Cuony>
    | * | | | | c4fce27 - Import mediawiki: First basic version. * Import page, with history and users (1 year, 10 months ago) <Maximilien Cuony>
    |/ / / / /  
    * | | | |   2671dbf - Merge pull request #267 from daonb/master (1 year, 11 months ago) <benjaoming>
    |\ \ \ \ \  
    | * | | | | c415572 - Fix testproject instructions (1 year, 11 months ago) <Benny Daon>
    |/ / / / /  
    * | | | | 3125d7d - Add explanation of current build status. (1 year, 11 months ago) <benjaoming>
    * | | | | f1a4aa6 - Travis should not test Django 1.4 against Python 3 (2 years ago) <benjaoming>
    * | | | | 9f265e5 - Fix #234 by adding @friedmud's suggestion and a max-height om <pre>'s (2 years ago) <benjaoming>
    * | | | | 44dcfdd - Fix filter() call in get_content_snippet not working on Python 2.7+ (2 years ago) <benjaoming>
    * | | | | e60cae5 - Adding prepopulated DB with front page article (2 years ago) <benjaoming>
    * | | | |   8c45e4a - Merge branch 'mastak-master' (2 years ago) <benjaoming>
    |\ \ \ \ \  
    | * \ \ \ \   c971cb4 - Merge branch 'master' of github.com:mastak/django-wiki into mastak-master (2 years ago) <benjaoming>
    | |\ \ \ \ \  
    |/ / / / / /  
    | * | | | | 6323f81 - replcae ArticleEmptyQuerySet to query_set().none(). Django 1.6 compatibilty (2 years ago) <Lubimov Igor>
    | | |/ / /  
    | |/| | |   
    * | | | | d6cf63f - once again correcting travis config and adding py3 fixed requirement for django_nyt (2 years ago) <benjaoming>
    * | | | | aa2980d - travis pip syntax err (2 years ago) <benjaoming>
    * | | | | 53fda7f - Only Django 1.4.2+ is support because of django-mptt (2 years ago) <benjaoming>
    * | | | | 3d37d9f - Only Django 1.4.2+ is support because of django-mptt (2 years ago) <benjaoming>
    * | | | | a219296 - Add list of known issues and include a note on Dj 1.4 and sorl with that. (2 years ago) <benjaoming>
    * | | | | abbacee - fix travis syntax err (2 years ago) <benjaoming>
    * | | | | 53cf3dc - Reconstructing Travis YML to only use selected combinations of django and python versions (2 years ago) <benjaoming>
    * | | | | 8dbcc7d - Travis requirements to get sorl 11.12.1b and fix django 1.7 beta from tarball instead of pip (2 years ago) <benjaoming>
    * | | | | 1c01ed8 - start testing south migrations again (2 years ago) <benjaoming>
    * | | | | 25a0206 - Fix broken images.south_migrations (0001_initial), add new .travis requirements (2 years ago) <benjaoming>
    * | | | | d1aeea8 - Adding draft notice to release notes (2 years ago) <benjaoming>
    * | | | |   9e518c2 - Merge branch 'master' of github.com:benjaoming/django-wiki (2 years ago) <benjaoming>
    |\ \ \ \ \  
    | * | | | | 3fc6745 - removing migration testing for now due to unknown erro (2 years ago) <benjaoming>
    * | | | | | fa16ac3 - removing migration testing for now due to unknown error (2 years ago) <benjaoming>
    |/ / / / /  
    * | | | | 9221c15 - add release note link (2 years ago) <benjaoming>
    * | | | | cf789ec - (Missing from previous commit) (2 years ago) <benjaoming>
    * | | | | ddf6aa3 - Refactor old South migration modules "migrations"->"south_migrations", add AppConfigs for future Django 1.7 (not supported yet), initial release notes, delete odd notifications migration that by mistake deletes the notifications subscriptions tables! (2 years ago) <benjaoming>
    * | | | | 102b015 - south migration and django 1.7 transitional support, remove django_notify and use django_nyt (2 years ago) <benjaoming>
    * | | | | bb82b46 - Tests should reflect forced lowercase paths. (2 years ago) <benjaoming>
    * | | | |   b032b61 - Merge branch 'master' of github.com:benjaoming/django-wiki (2 years ago) <benjaoming>
    |\ \ \ \ \  
    | * | | | | 8c45335 - Update article.py (2 years ago) <benjaoming>
    | * | | | | 4783abd - Only force new slugs to lowercase when not URL_CASE_SENSITIVE (2 years ago) <benjaoming>
    | * | | | | 42b6c49 - Fix confusing comment (2 years ago) <benjaoming>
    | * | | | |   7d45a29 - Merge pull request #260 from Jayflux/fixing_hyphen (2 years ago) <benjaoming>
    | |\ \ \ \ \  
    | | |/ / / /  
    | |/| | | |   
    | | * | | | 682a217 - added HTML5 pattern checking of lowercase and underscores (2 years ago) <Jason Williams>
    | | * | | | 3488ef1 - forcing cleanup server side (2 years ago) <Jason Williams>
    | | * | | | 5ae09e6 - fixing mistake made from last commit (2 years ago) <Jason Williams>
    | | * | | | c84a4b4 - This line should be removed, as it is removing the hyphen (2 years ago) <Jason Williams>
    | |/ / / /  
    * | | | | 38dc640 - Make tests run on django<1.6 (2 years ago) <benjaoming>
    | |_|/ /  
    |/| | |   
    * | | |   efae942 - Merge branch 'python3' of github.com:benjaoming/django-wiki into python3 (2 years ago) <benjaoming>
    |\ \ \ \  
    | * \ \ \   4040a48 - Merge pull request #254 from Mobeye/python3 (2 years, 1 month ago) <benjaoming>
    | |\ \ \ \  
    | | * | | | d43557a - Specified a version for sorl-thumbnails that is compatible with Python3 (2 years, 1 month ago) <Antonin Lenfant>
    | | * | | | 5c3a470 - Fix image upload when IMAGE_PATH_OBSCURIFY setting is enabled (2 years, 1 month ago) <Antonin Lenfant>
    | |/ / / /  
    | * | | |   ea3ef80 - Merge pull request #251 from spookylukey/python3 (2 years, 1 month ago) <benjaoming>
    | |\ \ \ \  
    | | * | | | 08c2fd8 - Fixed tox.ini dependencies for Python 3 support (2 years, 1 month ago) <Luke Plant>
    | | * | | | d6eaf90 - Added python3.3 environment to the envs to test in tox.ini (2 years, 1 month ago) <Luke Plant>
    | | * | | | f1de262 - Removed use of unicode_literals in migrations, because it causes many migrations to generate TypeError (2 years, 1 month ago) <Luke Plant>
    | | * | | |   0eec72b - Merge branch 'master' into python3 (2 years, 1 month ago) <Luke Plant>
    | | |\ \ \ \  
    | |/ / / / /  
    | * | | | | e66b853 - Move from __future__ to the beginning of the file (2 years, 3 months ago) <Russell-Jones>
    | * | | | |   fc91851 - Merge pull request #233 from benjaoming/master (2 years, 4 months ago) <Russell-Jones>
    | |\ \ \ \ \  
    | * \ \ \ \ \   7b19154 - Merge pull request #231 from benjaoming/master (2 years, 4 months ago) <Russell-Jones>
    | |\ \ \ \ \ \  
    | * | | | | | | 90e5a7b - Try change made by benjaoming on django-nyt (2 years, 4 months ago) <Russell-Jones>
    | * | | | | | | 7694ee4 - Move to python3-style unicode everywhere str() (2 years, 4 months ago) <Russell Jones>
    | * | | | | | | 29c4b56 - Move to python3-style unicode everywhere str() (2 years, 4 months ago) <Russell Jones>
    | * | | | | | | 18d0fc7 - Switch to python3-style unicode everywhere str() (2 years, 4 months ago) <Russell-Jones>
    | * | | | | | | 777b9aa - Switch to python3-style unicode everywhere str() (2 years, 4 months ago) <Russell-Jones>
    | * | | | | | |   4fc7f57 - Merge pull request #229 from benjaoming/master (2 years, 4 months ago) <Russell-Jones>
    | |\ \ \ \ \ \ \  
    | * | | | | | | | 2fc0f26 - Switch to Pillow and the dev version of sorl v12 (2 years, 4 months ago) <Russell-Jones>
    | * | | | | | | | e6e7343 - Add python 3.2 and 3.3 to trigger branch tci build (2 years, 4 months ago) <Russell-Jones>
    | * | | | | | | |   df496e9 - Merge branch 'master' into python3 (2 years, 4 months ago) <Russell Jones>
    | |\ \ \ \ \ \ \ \  
    | * | | | | | | | | dba4b67 - Convert filter iterator to list() to allow subscript (2 years, 4 months ago) <Russell Jones>
    | * | | | | | | | | 5a61e76 - Correct position of from future import (2 years, 4 months ago) <Russell Jones>
    | * | | | | | | | | 77fd906 - Start using from __future__ import unicode_literals everywhere Remove u from  u"" and u'' Start to remove calls to unicode() (2 years, 4 months ago) <Russell Jones>
    | * | | | | | | | | 93abe74 - Import only string_types from six (2 years, 4 months ago) <Russell Jones>
    | * | | | | | | | | c9b32ae - Replace basestring with six.string_types (2 years, 4 months ago) <Russell Jones>
    | * | | | | | | | | 58a3434 - Try to work around (necessary) absence of force_unicode in Django on python 3 (2 years, 4 months ago) <Russell Jones>
    | * | | | | | | | | b2fc091 - Add six to travis requirements.txt (2 years, 4 months ago) <Russell Jones>
    | * | | | | | | | |   ce3d62e - Merge branch 'py2and3' of github.com:Russell-Jones/django-wiki into python3 (2 years, 4 months ago) <benjaoming>
    | |\ \ \ \ \ \ \ \ \  
    | | * | | | | | | | | 61d3f10 - Stray tab (2 years, 4 months ago) <Russell Jones>
    | | * | | | | | | | | 6255677 - Convert iterator to list to allow extension with + operator (2 years, 4 months ago) <Russell Jones>
    | | * | | | | | | | | c56224d - Add six as a requirement (2 years, 4 months ago) <Russell Jones>
    | | * | | | | | | | | 8c4c091 - Missing colon (2 years, 4 months ago) <Russell Jones>
    | | * | | | | | | | | 8935aa0 - Add changes suggested by python-modernize (2 years, 4 months ago) <Russell Jones>
    * | | | | | | | | | | 3f88b01 - Fix py3 syntax error, refactor tests to be run with DiscoverRunner (2 years ago) <benjaoming>
    * | | | | | | | | | | 77413fe - Specified a version for sorl-thumbnails that is compatible with Python3 (2 years ago) <Antonin Lenfant>
    * | | | | | | | | | | d6ba371 - Fix image upload when IMAGE_PATH_OBSCURIFY setting is enabled (2 years ago) <Antonin Lenfant>
    * | | | | | | | | | | 4c54b9a - Fixed tox.ini dependencies for Python 3 support (2 years ago) <Luke Plant>
    * | | | | | | | | | | 606592b - Added python3.3 environment to the envs to test in tox.ini (2 years ago) <Luke Plant>
    * | | | | | | | | | | 2e4f15c - Removed use of unicode_literals in migrations, because it causes many migrations to generate TypeError (2 years ago) <Luke Plant>
    * | | | | | | | | | | d82e3b1 - Move from __future__ to the beginning of the file (2 years ago) <Russell-Jones>
    * | | | | | | | | | | a0d1862 - Try change made by benjaoming on django-nyt (2 years ago) <Russell-Jones>
    * | | | | | | | | | | e9c244f - Move to python3-style unicode everywhere str() (2 years ago) <Russell Jones>
    * | | | | | | | | | | 4f9bf51 - Move to python3-style unicode everywhere str() (2 years ago) <Russell Jones>
    * | | | | | | | | | | 2eb94b3 - Switch to python3-style unicode everywhere str() (2 years ago) <Russell-Jones>
    * | | | | | | | | | | 20e567a - Switch to python3-style unicode everywhere str() (2 years ago) <Russell-Jones>
    * | | | | | | | | | | 1b06ace - Switch to Pillow and the dev version of sorl v12 (2 years ago) <Russell-Jones>
    * | | | | | | | | | | 3ab06b2 - Add python 3.2 and 3.3 to trigger branch tci build (2 years ago) <Russell-Jones>
    * | | | | | | | | | | a9b3b5d - Convert filter iterator to list() to allow subscript (2 years ago) <Russell Jones>
    * | | | | | | | | | | e8c1345 - Correct position of from future import (2 years ago) <Russell Jones>
    * | | | | | | | | | | fd2475d - Start using from __future__ import unicode_literals everywhere Remove u from  u"" and u'' Start to remove calls to unicode() (2 years ago) <Russell Jones>
    * | | | | | | | | | | b74539f - Import only string_types from six (2 years ago) <Russell Jones>
    * | | | | | | | | | | 6ecb821 - Replace basestring with six.string_types (2 years ago) <Russell Jones>
    * | | | | | | | | | | 1baf410 - Try to work around (necessary) absence of force_unicode in Django on python 3 (2 years ago) <Russell Jones>
    * | | | | | | | | | | 6be734f - Add six to travis requirements.txt (2 years ago) <Russell Jones>
    * | | | | | | | | | | d0d585b - Stray tab (2 years ago) <Russell Jones>
    * | | | | | | | | | | 4b5a928 - Convert iterator to list to allow extension with + operator (2 years ago) <Russell Jones>
    * | | | | | | | | | | d88433d - Add six as a requirement (2 years ago) <Russell Jones>
    * | | | | | | | | | | 810581a - Missing colon (2 years ago) <Russell Jones>
    * | | | | | | | | | | 791888e - Add changes suggested by python-modernize (2 years ago) <Russell Jones>
    * | | | | | | | | | | a559f73 - typo (2 years, 1 month ago) <benjaoming>
    | |_|_|_|_|_|_|/ / /  
    |/| | | | | | | | |   
    * | | | | | | | | | 469d050 - notes on pull requests (2 years, 1 month ago) <benjaoming>
    * | | | | | | | | | 032b517 - Let us try adding a contribution documentent... (2 years, 1 month ago) <benjaoming>
    | |_|_|_|_|_|/ / /  
    |/| | | | | | | |   
    * | | | | | | | |   2340c32 - Merge pull request #250 from valberg/master (2 years, 2 months ago) <benjaoming>
    |\ \ \ \ \ \ \ \ \  
    | * | | | | | | | | 273b30c - Update installation.rst (2 years, 2 months ago) <valberg>
    | * | | | | | | | | 4247d6a - Fixing requirements list (2 years, 2 months ago) <valberg>
    |/ / / / / / / / /  
    * | | | | | | | |   76306f1 - Merge pull request #249 from andyreagan/patch-2 (2 years, 2 months ago) <benjaoming>
    |\ \ \ \ \ \ \ \ \  
    | * | | | | | | | | 134006e - Update installation.rst (2 years, 2 months ago) <Andy Reagan>
    * | | | | | | | | |   e523e00 - Merge pull request #248 from andyreagan/patch-1 (2 years, 2 months ago) <benjaoming>
    |\ \ \ \ \ \ \ \ \ \  
    | |/ / / / / / / / /  
    |/| | | | | | | | |   
    | * | | | | | | | | 5204edd - Update installation.rst (2 years, 2 months ago) <Andy Reagan>
    |/ / / / / / / / /  
    * | | | | | | | |   df22c9f - Merge pull request #241 from spookylukey/fix_transaction_management (2 years, 3 months ago) <benjaoming>
    |\ \ \ \ \ \ \ \ \  
    | * | | | | | | | | 457c487 - Merged wiki.compat into wiki.core.compat (2 years, 3 months ago) <Luke Plant>
    | * | | | | | | | | 086a36c - Added tox.ini and instructions, for easy running of tests in multiple environments (2 years, 3 months ago) <Luke Plant>
    | * | | | | | | | | 08312fc - Fix for issue #225 (exception when running with ATOMIC_REQUESTS), and the same applied to deleting subtrees (2 years, 3 months ago) <Luke Plant>
    | * | | | | | | | | 26ce59d - Added method to allow selected tests to be run, instead of running all. (2 years, 3 months ago) <Luke Plant>
    | * | | | | | | | | 6b300ac - Executable scripts 'setup.py' and 'runtests.py' (2 years, 3 months ago) <Luke Plant>
    | * | | | | | | | | f414e4a - Fixed incorrect indentation (2 years, 3 months ago) <Luke Plant>
    | | |_|_|_|_|/ / /  
    | |/| | | | | | |   
    * | | | | | | | | 8778a80 - Replace PIL with Pillow (2 years, 3 months ago) <benjaoming>
    |/ / / / / / / /  
    * | | | | | | |   11728df - Merge pull request #232 from vincentalvo/patch-1 (2 years, 4 months ago) <benjaoming>
    |\ \ \ \ \ \ \ \  
    | |_|_|_|_|/ / /  
    |/| | | | | | |   
    | * | | | | | | 3b944b0 - Image plugin: old revisions thumbnail error (2 years, 4 months ago) <vincentalvo>
    |/ / / / / / /  
    * | | | | | | 8444383 - do not build docs in build-sdist, it's not needed (2 years, 4 months ago) <benjaoming>
    * | | | | | | bf68a1c - Fix pluginbase incompatibility with django 1.6 #213 (2 years, 4 months ago) <benjaoming>
    | |_|_|/ / /  
    |/| | | | |   
    * | | | | | 1bedcb2 - Remove six (2 years, 4 months ago) <Russell-Jones>
    * | | | | | 4cbedac - travis-ci uses the branch committed to, reverted. (2 years, 4 months ago) <Russell-Jones>
    * | | | | | 6433be4 - Update requirements_1.6.txt (2 years, 4 months ago) <Russell-Jones>
    * | | | | | da8baf6 - Update .travis.yml (2 years, 4 months ago) <Russell-Jones>
    * | | | | | 53807f5 - add rtd conf env (2 years, 4 months ago) <benjaoming>
    * | | | | |   ecd2dec - Merge pull request #227 from spookylukey/easy_branding (2 years, 4 months ago) <benjaoming>
    |\ \ \ \ \ \  
    | |_|_|/ / /  
    |/| | | | |   
    | * | | | | 051ca6e - Corrected docs for easy branding method (2 years, 4 months ago) <Luke Plant>
    | * | | | | d1ea57b - Added easy way to brand the wiki, avoiding lots of copy and paste. (2 years, 4 months ago) <Luke Plant>
    | * | | | | 3b7420e - Beginnings of docs - converted from README (2 years, 4 months ago) <Luke Plant>
    |/ / / / /  
    * | | | | 2eaf23e - (tag: alpha/0.0.23, releases/0.0.23) Bump to 0.0.23 (2 years, 4 months ago) <benjaoming>
    * | | | | 57e9bcf - Fix #221 - not correctly inheriting some permissions, save() called on URLPath object instead of Article object! (2 years, 4 months ago) <benjaoming>
    |/ / / /  
    * | | |   489f2c5 - Merge pull request #220 from Russell-Jones/master (2 years, 4 months ago) <benjaoming>
    |\ \ \ \  
    | |/ / /  
    | * | | d36dbed - Add try catch block to test for and use if available new in 1.6 db transaction API (2 years, 4 months ago) <Russell Jones>
    |/ / /  
    * | |   9931ffd - Merge pull request #217 from tominardi/master (2 years, 5 months ago) <benjaoming>
    |\ \ \  
    | |/ /  
    |/| |   
    | * | 59a5614 - Edit french translations (2 years, 5 months ago) <tominardi>
    |/ /  
    * | ec5036c - (tag: alpha/0.0.22) bump version number (2 years, 5 months ago) <benjaoming>
    * | 38252b8 - #213 django 1.6 trouble fixed (2 years, 6 months ago) <benjaoming>
    * |   5538b39 - Merge branch 'master' of github.com:benjaoming/django-wiki (2 years, 6 months ago) <benjaoming>
    |\ \  
    | * | 5cab46e - Change requirements to use Pillow instead of PIL (2 years, 6 months ago) <benjaoming>
    | * | 127ada5 - Ah whatever... just delete everything about PIL!! (2 years, 6 months ago) <benjaoming>
    | * | 525b1b5 - PIL / Pillow related docs (2 years, 6 months ago) <benjaoming>
    | |/  
    * | 974db28 - Add PyCharm ignores (2 years, 6 months ago) <benjaoming>
    |/  
    * 40c6a4e - make README compatible with the pandoc translation to ReST (2 years, 6 months ago) <benjaoming>
    * ffd2216 - Readme and Changelog update (2 years, 6 months ago) <benjaoming>
    * 2f59ecb - version bump to 0.0.21 (2 years, 6 months ago) <benjaoming>
    * 6e47242 - Fix #191 - introduce DRY in plugins.notifications default_url (2 years, 6 months ago) <benjaoming>
    * 363f50a - Fix #206 by upgrading markitup to newer version (2 years, 6 months ago) <benjaoming>
    * 34ac301 - Fix #207 and upgrade to jquery 1.10.2 (2 years, 6 months ago) <benjaoming>
    * 57a3c97 - Fix #211 by adding a bit more clarity on the context variable handling (2 years, 6 months ago) <benjaoming>
    * e08b54d - Fix bug in decorator causing double reverse lookups (2 years, 6 months ago) <benjaoming>
    * e4d904e - Remove tests from plugins that are just stub implementations and not django 1.6 compat (2 years, 6 months ago) <benjaoming>
    * a71b0ff - README updated (2 years, 6 months ago) <benjaoming>
    * a5395e8 - syntax highlighting for README (2 years, 6 months ago) <benjaoming>
    * 233bcf4 - Writing a few words on usage (2 years, 6 months ago) <benjaoming>
    * 1db4378 - Add a screenshot (2 years, 6 months ago) <benjaoming>
    * ab87c5a - Adding Travis tests for Django 1.6 (2 years, 6 months ago) <benjaoming>
    * f1bad2d - automatically generate docs and CHANGELOG.md (2 years, 6 months ago) <benjaoming>
    * b757c6d - Trying out a markdown formatted auto-gererated for new releases CHANGELOG (2 years, 6 months ago) <benjaoming>
    * 22936c3 - Automating version number for sphinx (2 years, 6 months ago) <benjaoming>
    * f232fd6 - django 1.6 fix for #191 - ArticleRevision.get_latest_by should be single field, not tuple (2 years, 6 months ago) <benjaoming>
    * cc31f07 - django 1.6 and #191 BooleanField now has NULL value (2 years, 6 months ago) <benjaoming>
    *   d0ea990 - Merge pull request #208 from stratatech/master (2 years, 6 months ago) <benjaoming>
    |\  
    | * d8e872f - Russian translations fixes (2 years, 6 months ago) <sminozhenko>
    | * 13c3e06 - Remove unnecessary lamba function (2 years, 6 months ago) <sminozhenko>
    | * 164b416 - Russion translations + some missing label added + problem with transaltions in django_notify.settings.py (2 years, 6 months ago) <sminozhenko>
    |/  
    *   b4d3be8 - Merge pull request #202 from rgcarrasqueira/master (2 years, 6 months ago) <benjaoming>
    |\  
    | * 8ede8b8 - Bugfix request method is not found Django 1.4.7 (2 years, 6 months ago) <Rogério Carrasqueira>
    | * 02f4bbe - Changing mptt to 0.5.3 (2 years, 6 months ago) <Rogério Carrasqueira>
    | * e146a5d - Become compatible with django-cms 2.4.2 due django-sekizai (2 years, 6 months ago) <Rogério Carrasqueira>
    * |   08758a6 - Merge pull request #203 from TomLottermann/master (2 years, 6 months ago) <benjaoming>
    |\ \  
    | |/  
    |/|   
    | * ef4cccf - Updated translation. Fixed some minor issues. (2 years, 6 months ago) <Thomas Lottermann>
    |/  
    * af767e3 - Instruction text for direct pip installation from git (2 years, 7 months ago) <benjaoming>
    *   6104404 - Merge pull request #199 from TomLottermann/master (2 years, 7 months ago) <benjaoming>
    |\  
    | * 29a03a3 - indentation fixed (2 years, 7 months ago) <Thomas Lottermann>
    | * d3b52cf - pagination broke with bootstrap 3. It now works again! (2 years, 7 months ago) <Thomas Lottermann>
    |/  
    *   db32a3e - Merge pull request #198 from TomLottermann/master (2 years, 7 months ago) <benjaoming>
    |\  
    | *   be3b35d - Merge remote-tracking branch 'upstream/master' (2 years, 7 months ago) <Thomas Lottermann>
    | |\  
    | |/  
    |/|   
    * | d07ba79 - fix #193 - only add style to input type=text/password (2 years, 7 months ago) <benjaoming>
    * | c8d9307 - Fix [TOC] compatibility with custom ids and add support for [[WikiLink]] #179 (2 years, 7 months ago) <benjaoming>
    * | c73d331 - remove bogus highlight plugin (2 years, 7 months ago) <benjaoming>
    * |   809a12f - Merge branch 'master' of github.com:benjaoming/django-wiki (2 years, 7 months ago) <benjaoming>
    |\ \  
    | * \   d956400 - Merge pull request #190 from yedpodtrzitko/master (2 years, 7 months ago) <benjaoming>
    | |\ \  
    | | * | 085d4aa - bump translations (2 years, 9 months ago) <yed_>
    | | * | e4e655e - show info about missing root instead of redirect to login (fix #174) (2 years, 9 months ago) <yed_>
    * | | | 92cddce - add codehilite to default markdown extensions and close #134 (2 years, 7 months ago) <benjaoming>
    |/ / /  
    * | |   e5cbdf4 - Merge branch 'master' of github.com:benjaoming/django-wiki (2 years, 7 months ago) <benjaoming>
    |\ \ \  
    * | | | aca44f0 - fix #197 - use twitter typeahead (2 years, 7 months ago) <benjaoming>
    * | | | 9716942 - ignore haystack test indexes (2 years, 7 months ago) <benjaoming>
    | | | * b7c24ed - Group and owner can be null. The index must support this! (2 years, 7 months ago) <Thomas Lottermann>
    | | |/  
    | |/|   
    | * |   51019fc - Merge pull request #192 from jbazik/master (2 years, 8 months ago) <benjaoming>
    | |\ \  
    | | * | f1560a3 - Use a private instance of sorl.thumbnails. (2 years, 8 months ago) <John Bazik>
    | |/ /  
    | * |   2314aa0 - Merge pull request #189 from yedpodtrzitko/master (2 years, 9 months ago) <benjaoming>
    | |\ \  
    | | |/  
    | | *   05a5f53 - Merge remote-tracking branch 'orig/master' (2 years, 9 months ago) <yed_>
    | | |\  
    | | |/  
    | |/|   
    | * |   0cb2ca2 - Merge pull request #188 from yedpodtrzitko/master (2 years, 9 months ago) <benjaoming>
    | |\ \  
    |/ / /  
    | | * 30c45e2 - _change revision_ as a class-based view (2 years, 9 months ago) <yed_>
    | |/  
    | * 10a4457 - create root as a class-based view (2 years, 9 months ago) <yed_>
    |/  
    *   9528bf7 - Merge branch 'master' of github.com:benjaoming/django-wiki (2 years, 9 months ago) <benjaoming>
    |\  
    | * 04ce91f - Update local.py (2 years, 9 months ago) <benjaoming>
    * | 2c35ea7 - urlize also on last-of-line urls + fix icon (2 years, 9 months ago) <benjaoming>
    |/  
    * 8fd557c - Fix #186 -- add empty local.py file (2 years, 9 months ago) <benjaoming>
    *   8af2a61 - Merge branch 'master' of github.com:benjaoming/django-wiki (2 years, 9 months ago) <benjaoming>
    |\  
    | * 8ffd8f0 - Fix #178 - improve urlize regex to accept everything after a domain, except spaces, [, and ( (2 years, 9 months ago) <benjaoming>
    * | 05ecdbb - Fix #178 - improve urlize regex to accept everything after a domain, except spaces, [, and ( (2 years, 9 months ago) <benjaoming>
    |/  
    * 2108a32 - grid layout on all form-action occurences (2 years, 9 months ago) <benjaoming>
    * 5a90cfe - more issues in bootstrap 3 form widgets (2 years, 9 months ago) <benjaoming>
    * bb89355 - textarea height and edit page button layout (2 years, 9 months ago) <benjaoming>
    * 4aef17a - Fix #181 and #183 -- responsive modals, prepend for form inputs, form controls fixed for horizontal and vertical layouts (2 years, 9 months ago) <benjaoming>
    * eb21b9d - bootstrap 3 compat on attachments plugin (2 years, 9 months ago) <benjaoming>
    * 826b082 - fix 404 on respond.js (2 years, 9 months ago) <benjaoming>
    *   3253098 - Merge branch 'master' of github.com:benjaoming/django-wiki (2 years, 9 months ago) <benjaoming>
    |\  
    | *   5b34a24 - Merge pull request #185 from vezjakv/master (2 years, 9 months ago) <benjaoming>
    | |\  
    | | * cbb815a - Init std.out stream handler compatable with Python 2.6 (2 years, 9 months ago) <vezjakv>
    | |/  
    | * 27cc33c - Update README.md (2 years, 9 months ago) <benjaoming>
    | * d059edb - SHA digest should display as link (2 years, 9 months ago) <benjaoming>
    | * 515a1b7 - News update (2 years, 9 months ago) <benjaoming>
    | * a594811 - Github Markdown broken on multiple comments in one line (2 years, 9 months ago) <benjaoming>
    * | 8e77f06 - add codehilite note in README and a testproject settings module (2 years, 9 months ago) <benjaoming>
    * | 06aa0e2 - add codehilite CSS to enable syntax highlighting for the codehilite Markdown extension (2 years, 9 months ago) <benjaoming>
    * | e4382c8 - strip tags from Haystack searches (2 years, 9 months ago) <benjaoming>
    * | 0cf10f5 - fix some more btn-default (2 years, 9 months ago) <benjaoming>
    * | 47dee16 - fix btn-default in some other cases (2 years, 9 months ago) <benjaoming>
    * | 9ccb216 - fix bootstrap btn-default class (2 years, 9 months ago) <benjaoming>
    |/  
    * d8149a6 - fix #182 - bootstrap problem, not html (2 years, 9 months ago) <benjaoming>
    * be42a26 - include font files in MANIFEST (2 years, 9 months ago) <benjaoming>
    * d077af2 - responsive search form (2 years, 9 months ago) <benjaoming>
    * fbccb07 - Fix search form on chromium (2 years, 9 months ago) <benjaoming>
    * 657b8f9 - remove old bootstrap files (2 years, 9 months ago) <benjaoming>
    * 34b9117 - refactor bootstrap grid layout (2 years, 9 months ago) <benjaoming>
    * b919d54 - Upgrade to Bootstrap 3 RC1, add font-awesome, lots of refactoring (2 years, 9 months ago) <benjaoming>
    * 204cc43 - make __init__.py always try to import settings.local (2 years, 9 months ago) <benjaoming>
    * 91064d6 - Add SECRET_KEY to standard settings so testproject runs out of the box (2 years, 9 months ago) <benjaoming>
    * e624b61 - Remove old settings_local.py (2 years, 9 months ago) <benjaoming>
    * 04f131c - Add #django-wiki IRC channel - yay :) (2 years, 9 months ago) <benjaoming>
    * 0f3bf03 - add setting WIKI_ACCOUNT_SIGNUP_ALLOWED (2 years, 9 months ago) <benjaoming>
    * ebe1503 - Don't be verbose while scanning for plugins (2 years, 9 months ago) <benjaoming>
    * 384fb62 - Fix #23 - move model registration from taking place within wiki.models to wiki.urls -- after all apps and models have been loaded (2 years, 10 months ago) <benjaoming>
    * fcce3ce - cleanup (2 years, 10 months ago) <benjaoming>
    * 5ff6fac - Fix #160 by allowing django-sendfile to be plugged in through settings.USE_SENDFILE (2 years, 10 months ago) <benjaoming>
    * 0418642 - Fix #162 -- add filter_exclude to notify() (2 years, 10 months ago) <benjaoming>
    * 02cb4d2 - Fix #164 by always setting a timeout for notification updates (2 years, 10 months ago) <benjaoming>
    *   0bc8e32 - Merge branch 'master' of github.com:benjaoming/django-wiki (2 years, 10 months ago) <benjaoming>
    |\  
    | * 0c148d3 - make possible for moderators to replace attachments (2 years, 10 months ago) <benjaoming>
    * | 7846c81 - make possible for moderators to replace attachments, also fix #170, and remove catching all exceptions (2 years, 10 months ago) <benjaoming>
    |/  
    * 8f65dd2 - Travis settings for test project (2 years, 10 months ago) <benjaoming>
    *   3f3c903 - Fix #173 by letting articles refer to other article's attachments while checking the permissions of the original article owner (2 years, 10 months ago) <benjaoming>
    |\  
    | * b9981cf - Updating travis test to use new settings layout (2 years, 10 months ago) <benjaoming>
    * | 0090335 - Trying a new travis configuration since the PYTHON_PATH does not understand testproject.settings (2 years, 10 months ago) <benjaoming>
    |/  
    * 112bba7 - cleanup (2 years, 10 months ago) <benjaoming>
    * 88030a1 - Add Haystack search plugin (NB! Whoosh backend is broken upstream) (2 years, 10 months ago) <benjaoming>
    * e21da47 - script to migrate south migrations to a custom auth user model (has already been run on wiki.migrations) (2 years, 10 months ago) <benjaoming>
    * 58a46b8 - Refactore testproject.settings to accommodate more scenarios (2 years, 10 months ago) <benjaoming>
    * a4e3ebf - make SEARCH_VIEW configurable from conf.settings (2 years, 10 months ago) <benjaoming>
    * 24271db - cleanup unnecessary file (2 years, 10 months ago) <benjaoming>
    * 810bd00 - Automatically generate README.rst for PyPi (2 years, 10 months ago) <benjaoming>
    *   0c49222 - Merge branches 'master' and 'haystack' of github.com:benjaoming/django-wiki into haystack (2 years, 10 months ago) <benjaoming>
    |\  
    | *   b9d969d - Merge pull request #172 from holdenweb/patch-1 (2 years, 10 months ago) <benjaoming>
    | |\  
    | | * bcb47c9 - Update README.md (2 years, 10 months ago) <Steve Holden>
    | |/  
    | *   3a06ff1 - Merge pull request #168 from TomLottermann/master (2 years, 11 months ago) <benjaoming>
    | |\  
    | | *   a448f74 - Merge remote-tracking branch 'upstream/master' (2 years, 11 months ago) <Thomas Lottermann>
    | | |\  
    | | |/  
    | |/|   
    | * | 39ecbdf - Cleanup 'admin' slug error message (2 years, 11 months ago) <benjaoming>
    | * |   d9b2a5b - Merge pull request #166 from BenMarchant/patch-2 (2 years, 11 months ago) <benjaoming>
    | |\ \  
    | | * | 0449a29 - Visitor cannot use admin as a slug (just in case !) (2 years, 11 months ago) <BenMarchant>
    | |/ /  
    | * |   3d573b0 - Merge pull request #165 from BenMarchant/patch-1 (2 years, 11 months ago) <benjaoming>
    | |\ \  
    | | * | be728b0 - Fixed: "wiki_footer_prepend block" (2 years, 11 months ago) <BenMarchant>
    | |/ /  
    | | * 7b40385 - fixed non-found absolute wiki urls (2 years, 11 months ago) <Thomas Lottermann>
    * | | 2c1e7c1 - Fix Django 1.4 incompatibility (2 years, 10 months ago) <benjaoming>
    * | |   9c31dc3 - Merge branch 'haystack-search' of git://github.com/jdcaballero/django-wiki into jdcaballero-haystack-search (2 years, 11 months ago) <benjaoming>
    |\ \ \  
    | |/ /  
    |/| |   
    | * |   784f8d6 - Merge pull request #1 from TomLottermann/haystack-search (2 years, 11 months ago) <jdcaballero>
    | |\ \  
    | | * | 6108d30 - Minor fix (2 years, 11 months ago) <Thomas Lottermann>
    | | * | e10d573 - Haystack 2.0 broke some stuff (site did not exist). This is fixed now. Furthermore we can use the highlighter by haystack. It does some stuff nicer than django-wikis (2 years, 11 months ago) <Thomas Lottermann>
    | | * | e68272c - Some minor cleanup and same redirect behaviour on anonymous access (2 years, 11 months ago) <Thomas Lottermann>
    | | * |   a1a25c2 - Merge remote-tracking branch 'jdcaballero/haystack-search' into haystack-search (2 years, 11 months ago) <Thomas Lottermann>
    | | |\ \  
    | | |/ /  
    | |/| /   
    | | |/    
    | * | 4035783 - Permissions bare implementation (3 years, 1 month ago) <Juan Diego Caballero>
    | * | ba667f1 - Paginator used to show the number of results (3 years, 2 months ago) <Juan Diego Caballero>
    | * | 54c14bb - Initial Implementation of Search using Haystack (3 years, 2 months ago) <Juan Diego Caballero>
    * | | dfe7be5 - hand empty notifications settings (2 years, 11 months ago) <benjaoming>
    * | | d7df0af - pep8 cleanup (2 years, 11 months ago) <benjaoming>
    * | | ed9d853 - Add notification interval to Article Settings page + New Notifications Settings page (2 years, 11 months ago) <benjaoming>
    * | | 1d4faa9 - get_absolute_path added to Article model (2 years, 11 months ago) <benjaoming>
    * | | 0a946c5 - Bootstrap 2.3.2 added and compatibility changes for dropdown menu (2 years, 11 months ago) <benjaoming>
    * | | c24c882 - cleanup bootstrap (2 years, 11 months ago) <benjaoming>
    | |/  
    |/|   
    * | c259b31 - Alter plugin API: BasePlugin.urlpatterns is now a dictionary (2 years, 11 months ago) <benjaoming>
    * | ca59f20 - undo, only bad inheritance results in need of self.request set here (2 years, 11 months ago) <benjaoming>
    * | 8bab47d - self.request on ArticleMixin view to allow for parent dispatch methods assuming its existence (2 years, 11 months ago) <benjaoming>
    * | 0b9c2c5 - shorten database settings (2 years, 11 months ago) <benjaoming>
    * | ac04cb6 - fix missing refactoring on renamed template block wiki_pagetitle (2 years, 11 months ago) <benjaoming>
    * |   dfb9456 - Merge branch 'master' of github.com:benjaoming/django-wiki (2 years, 11 months ago) <benjaoming>
    |\ \  
    | * | 00e4713 - Update README.md (2 years, 11 months ago) <benjaoming>
    * | | 0d13578 - Fix #161 (mark accumulated notifications is_emailed=False) + clean up code + make notification email nicer (2 years, 11 months ago) <benjaoming>
    |/ /  
    * |   a84eb16 - Merge branch 'master' of github.com:benjaoming/django-wiki (2 years, 11 months ago) <benjaoming>
    |\ \  
    | * | b78edee - Update README.md (2 years, 11 months ago) <benjaoming>
    * | | 00cf45b - (tag: alpha/0.0.20) Bump to 0.0.20 (2 years, 11 months ago) <benjaoming>
    |/ /  
    * |   cc537a5 - Merge pull request #159 from TomLottermann/master (2 years, 11 months ago) <benjaoming>
    |\ \  
    | * | 1bc5e48 - The management command now loads the language see https://docs.djangoproject.com/en/dev/howto/custom-management-commands/ for more details (2 years, 11 months ago) <Thomas Lottermann>
    | * | 5c53280 - adding missing manifest information. language files were not included in the build. (2 years, 11 months ago) <Thomas Lottermann>
    |/ /  
    * |   10c6444 - Merge pull request #157 from crazyzubr/master (2 years, 11 months ago) <benjaoming>
    |\ \  
    | * | 6575a4a - simplify notify_settings (2 years, 11 months ago) <crazyzubr>
    | * | dca3618 - fix notify_settings confuse (2 years, 11 months ago) <crazyzubr>
    | * | f00af80 - filehandler django_notify in daemon mode (2 years, 11 months ago) <crazyzubr>
    * | |   eabe615 - Merge pull request #156 from crazyzubr/master (2 years, 11 months ago) <benjaoming>
    |\ \ \  
    | |/ /  
    | * | 3f08aec - fix (2 years, 11 months ago) <crazyzubr>
    | * | 1006454 - add russian translation from django-notify (2 years, 11 months ago) <crazyzubr>
    * | |   4fe5e47 - Merge pull request #155 from crazyzubr/master (2 years, 11 months ago) <benjaoming>
    |\ \ \  
    | |/ /  
    | * | 90dde5a - fix errata (locale ru) (2 years, 11 months ago) <crazyzubr>
    | * | 2d4eae2 - update locale ru (.po and .mo) (2 years, 11 months ago) <crazyzubr>
    | * | fe8c7bd - Create django.po (2 years, 11 months ago) <crazyzubr>
    |/ /  
    * |   69d209d - Merge pull request #153 from TomLottermann/master (3 years ago) <benjaoming>
    |\ \  
    | * | fd0ef6a - Updated german translations (3 years ago) <TomLottermann>
    |/ /  
    * |   1b7c241 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years ago) <benjaoming>
    |\ \  
    | * | 8b93d34 - Update TEMPLATE_CONTEXT_PROCESSORS instructions (3 years ago) <benjaoming>
    * | | 71880a2 - #145 do not break when AUTH_USER_MODEL is set on django<1.5 project (3 years ago) <benjaoming>
    * | | ad7b664 - Respect custom models (NB! current django 1.5.1 breaks wiki.views.accounts) #145 (3 years ago) <benjaoming>
    * | | 68e3478 - Remove spaces (3 years ago) <benjaoming>
    * | | 4e32ab6 - Add test suite that supports settings.AUTH_USER_MODEL and testing of South migrations #145 (3 years ago) <benjaoming>
    * | | 670c4d2 - #145 - add compatibility layer for importing users (3 years ago) <benjaoming>
    |/ /  
    * | 60c24e6 - Remove revisions to shrink prepopulated test db (3 years ago) <benjaoming>
    * | 03f0cc5 - vacuum sqlite test database and add new migrations (3 years ago) <benjaoming>
    * | e2d188b - Remember to call parent UserCreationForm.clean - fix username not tested for uniqueness in account handling (3 years ago) <benjaoming>
    * | 5d4c545 - BaseRevisionMixin.previous_revision: Allow deletion of Revisions by setting back-referenced revisions to NULL such that future revisions are not cascade deleted. (3 years ago) <benjaoming>
    * | e506c09 - Issue #145 - Add support for settings.AUTH_USER_MODEL both in model ForeignKey fields and South migrations. Backwards-compatible. (3 years ago) <benjaoming>
    * | 84c07e8 - #151 - missing translation calls (3 years ago) <benjaoming>
    * |   ec82837 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years ago) <benjaoming>
    |\ \  
    | * \   7a2103d - Merge pull request #150 from xiaclo/patch-1 (3 years ago) <benjaoming>
    | |\ \  
    | | * | ee85908 - Remove space from urlify.js path (3 years ago) <xiaclo>
    | |/ /  
    | * |   7e0f0a3 - Merge pull request #149 from TomLottermann/master (3 years ago) <benjaoming>
    | |\ \  
    | | * | 8782c84 - Slug stays fixed if the article already has a initial slug (3 years ago) <TomLottermann>
    | * | |   b5acff0 - Merge pull request #147 from TomLottermann/master (3 years ago) <benjaoming>
    | |\ \ \  
    | | |/ /  
    | | * |   6a69d88 - Merge remote-tracking branch 'upstream/master' (3 years ago) <TomLottermann>
    | | |\ \  
    | | |/ /  
    | |/| |   
    | * | | 7f172fb - Update README.md (3 years ago) <benjaoming>
    | | * | 493305b - Added wrapSelection to editor.js (3 years ago) <TomLottermann>
    * | | | 5b6c496 - (tag: alpha/0.0.19) Version bump (3 years ago) <benjaoming>
    |/ / /  
    * | | 61b3c61 - Make the urlize parser more strict (3 years ago) <benjaoming>
    * | | 36f3640 - add back anon read access to test main article (3 years, 1 month ago) <benjaoming>
    * | | 31e2e60 - font size in blockquotes (3 years, 1 month ago) <benjaoming>
    * | | 83c72bf - lock main article in the test project (3 years, 1 month ago) <benjaoming>
    * | | dec9335 - Add attr_list to allow e.g. custom Header ids for custom references to header sections (3 years, 1 month ago) <benjaoming>
    * | | 1a896ed - Markdown needs to be >2.2.0 due to 2.1.1 headerid extension tested broken with newer ElemenTree versions (3 years, 1 month ago) <benjaoming>
    * | | 09e8af9 - less blahblah on the contribution stuff (3 years, 1 month ago) <benjaoming>
    * | | 78bf232 - remove pip --use-mirrors (3 years, 1 month ago) <benjaoming>
    * | |   6a1217c - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 1 month ago) <benjaoming>
    |\ \ \  
    | * \ \   60bcbbd - Merge pull request #143 from TomLottermann/master (3 years, 1 month ago) <benjaoming>
    | |\ \ \  
    | | |/ /  
    | | * |   9ca5afb - Merge branch 'master' of github.com:TomLottermann/django-wiki (3 years, 1 month ago) <TomLottermann>
    | | |\ \  
    | | | * | d4ce6ca - Fixed wrong icon when deleting article (3 years, 1 month ago) <TomLottermann>
    | | * | | 06dc3ed - Fixed wrong icon when deleting article (3 years, 1 month ago) <TomLottermann>
    | | |/ /  
    | * | |   d280dd4 - Merge pull request #142 from TomLottermann/master (3 years, 1 month ago) <benjaoming>
    | |\ \ \  
    | | |/ /  
    | | * | a705f64 - version fix (3 years, 1 month ago) <TomLottermann>
    | | * | 4cbc633 - version fix (3 years, 1 month ago) <TomLottermann>
    | | * | 7188641 - Added translations for django_notify (3 years, 1 month ago) <TomLottermann>
    | | * | acba7f7 - Respected changes, reformatted the lines (3 years, 1 month ago) <TomLottermann>
    | |/ /  
    * | | c2f450b - fix SimplePlugin constructor - pull #144 (3 years, 1 month ago) <benjaoming>
    |/ /  
    * |   ca5e28a - pull #141 - remove old test mechanism, try adding Warning failure (3 years, 1 month ago) <benjaoming>
    |\ \  
    | * | 16f8e0b - pull #141 - add manage.py test + Django 1.5 to Travis config (3 years, 1 month ago) <benjaoming>
    * | | e36f597 - pull #141 - remove old test mechanism, try adding Warning failure (3 years, 1 month ago) <benjaoming>
    |/ /  
    * |   177bf3c - Merge pull request #141 from hynekcer/master (3 years, 1 month ago) <benjaoming>
    |\ \  
    | * | eecd8a5 - Fixed on_article_delete_clear_cache. Some articles in the cache were not cleared and tests failed. (3 years, 1 month ago) <Hynek Cernoch>
    | * | 2ad0694 - Added tests for clearing cache and for updating article_list (3 years, 1 month ago) <Hynek Cernoch>
    | * | effc58a - Fixed on_article_delete if the article has children. (3 years, 1 month ago) <Hynek Cernoch>
    | * | 44e4d7a - Added more tests and refactored the the first one. (3 years, 1 month ago) <Hynek Cernoch>
    | * | 6dc14a1 - Fixed RuntimeWarning by replacing naive datetime by utc (3 years, 1 month ago) <Hynek Cernoch>
    * | | d746543 - #140 - Markdown 2.2/2.3 API change - do not rely on markdown.extensions.headerid.unique (3 years, 1 month ago) <benjaoming>
    |/ /  
    * | f6eb8be - French translation - changed msg id (att. pull #138) (3 years, 1 month ago) <benjaoming>
    * | 8332ab6 - pull #139 - form data from args or kwargs (3 years, 1 month ago) <benjaoming>
    * |   1aa8eb2 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 1 month ago) <benjaoming>
    |\ \  
    | * | 4f0ef1a - pull #139 - form data from args or kwargs (3 years, 1 month ago) <benjaoming>
    * | | 09f91ea - pull #139 - form data from args or kwargs (3 years, 1 month ago) <benjaoming>
    |/ /  
    * |   159025b - Merge pull request #139 from hynekcer/master (3 years, 1 month ago) <benjaoming>
    |\ \  
    | * | 634c3c0 - Revert "Fixed posting data to views.article.Preview" (3 years, 1 month ago) <Hynek Cernoch>
    | * | 1bba4ec - Added recursion test for the current bug in preview. (3 years, 1 month ago) <Hynek Cernoch>
    |/ /  
    * |   c3bbc37 - Do not use kwargs for permission methods (3 years, 1 month ago) <benjaoming>
    |\ \  
    | * | 2d7957a - Do not use kwargs for permission methods (3 years, 1 month ago) <benjaoming>
    * | | 37d9939 - Do not use kwargs for permission methods (3 years, 1 month ago) <benjaoming>
    |/ /  
    * | d37e09c - #137 place permission logic ONLY in core.permissions and make article.can_read and article.can_write configurable (3 years, 1 month ago) <benjaoming>
    * |   fdd36cd - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 1 month ago) <benjaoming>
    |\ \  
    | * \   de55506 - Merge pull request #138 from jdcaballero/master (3 years, 1 month ago) <benjaoming>
    | |\ \  
    | | * \   054b3af - Merge remote-tracking branch 'origin/master' (3 years, 1 month ago) <Juan Diego Caballero>
    | | |\ \  
    | | |/ /  
    | |/| |   
    | * | | 84dc39f - More clear PIL instructions. (3 years, 1 month ago) <benjaoming>
    | | * | 5468b9a - Spanish translations added. (3 years, 1 month ago) <Juan Diego Caballero>
    | | * | b74303e - Do not use HttpResponseRedirectBase anyways, just check status_code (3 years, 1 month ago) <benjaoming>
    | | * | 43dbdd9 - fix imporerror for HttpResponseRedirectBase (3 years, 1 month ago) <benjaoming>
    | | * | bc0eff8 - JSON view can return HttpResponseRedirect (3 years, 1 month ago) <benjaoming>
    | | * | 71a6457 - changing apt-get to use python-imaging (3 years, 1 month ago) <Dennis Coldwell>
    | | * | f76bc85 - adding PIL pre-req documentation (3 years, 1 month ago) <Dennis Coldwell>
    * | | | 71c59d6 - fix wrong form target on clicking 'Switch to selected version' + modal window height (3 years, 1 month ago) <benjaoming>
    |/ / /  
    * | | beb7571 - Do not use HttpResponseRedirectBase anyways, just check status_code (3 years, 1 month ago) <benjaoming>
    * | | 6da0fd9 - fix imporerror for HttpResponseRedirectBase (3 years, 1 month ago) <benjaoming>
    * | | 3f1ac96 - JSON view can return HttpResponseRedirect (3 years, 1 month ago) <benjaoming>
    * | |   6a9539d - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 1 month ago) <benjaoming>
    |\ \ \  
    | |/ /  
    |/| |   
    | * |   f4f3a1d - Merge pull request #135 from coldwd/patch-1 (3 years, 1 month ago) <benjaoming>
    | |\ \  
    | | * | ef83744 - changing apt-get to use python-imaging (3 years, 1 month ago) <Dennis Coldwell>
    | | * | 4cf921f - adding PIL pre-req documentation (3 years, 1 month ago) <Dennis Coldwell>
    | |/ /  
    * | | 0ff3fd4 - Fix #136 (3 years, 1 month ago) <benjaoming>
    |/ /  
    * | e9bd946 - add clearfix for article tocs and indexes (3 years, 1 month ago) <benjaoming>
    * | 5fdb93d - fix #130 - display disabled dropdown when no assignment permission (3 years, 1 month ago) <benjaoming>
    * | 45cd25e - clean up block tags to be prefixed 'wiki_*' (3 years, 1 month ago) <benjaoming>
    * |   0911c58 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 1 month ago) <benjaoming>
    |\ \  
    | * \   914ecf5 - Merge pull request #132 from hynekcer/master (3 years, 1 month ago) <benjaoming>
    | |\ \  
    | | * | 8f60a11 - Fixed typo in admin - Article revision list columns (3 years, 1 month ago) <Hynek Cernoch>
    | |/ /  
    | * | a908af4 - Update README.md (3 years, 1 month ago) <benjaoming>
    * | | 0344928 - Update to Bootstrap 2.3.1 and simplify LESS import statements (3 years, 1 month ago) <benjaoming>
    |/ /  
    * | 428d236 - (tag: alpha/0.0.18) Bump to 0.0.18 (3 years, 1 month ago) <benjaoming>
    * | 85602fe - Fix #125 - missing redirect call (3 years, 1 month ago) <benjaoming>
    * |   807611b - Merge pull request #131 from daltonmatos/translation/pt_BR (3 years, 1 month ago) <benjaoming>
    |\ \  
    | * | 5779039 - Adding translation for pt_BR (3 years, 1 month ago) <Dalton Barreto>
    |/ /  
    * |   2cd0dbe - Merge pull request #129 from TomLottermann/master (3 years, 2 months ago) <benjaoming>
    |\ \  
    | * | dc6a2aa - reset readme and removed mo ignorance from gitignore, since it is needed (3 years, 2 months ago) <TomLottermann>
    | * | 548cc81 - complete set of languages (3 years, 2 months ago) <TomLottermann>
    | * | 62b37b3 - compiled recent version (3 years, 2 months ago) <TomLottermann>
    | * | 757f24a - Plugins are a WIP (3 years, 2 months ago) <TomLottermann>
    | * | b694a89 - right names (3 years, 2 months ago) <TomLottermann>
    | * | 3339ae4 - fixes to the manifest (3 years, 2 months ago) <TomLottermann>
    | * | 69a4b2d - german locale (3 years, 2 months ago) <TomLottermann>
    | * | 9da762d - Compilation of german locale (3 years, 2 months ago) <TomLottermann>
    | * | d9b997b - initial translation done (without the plugins) (3 years, 2 months ago) <TomLottermann>
    | * | a6182dd - start of translations (3 years, 2 months ago) <TomLottermann>
    | * | 59b6558 - start of translations (3 years, 2 months ago) <TomLottermann>
    | * | 8efc4bd - readme changed (3 years, 2 months ago) <TomLottermann>
    |/ /  
    * |   75a0581 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 2 months ago) <benjaoming>
    |\ \  
    | * | 2b28521 - Update README.md (3 years, 2 months ago) <benjaoming>
    | * |   17b15d9 - Merge pull request #124 from SacNaturalFoods/master (3 years, 2 months ago) <benjaoming>
    | |\ \  
    | | * | 3add05a - fixed _clear_ancestor_cache call (3 years, 2 months ago) <tschmidt>
    | * | |   bc57765 - Merge pull request #122 from SacNaturalFoods/master (3 years, 2 months ago) <benjaoming>
    | |\ \ \  
    | | |/ /  
    | | * | 088e2de - moved article save and delete clear cache signal handlers to Article model (3 years, 2 months ago) <tschmidt-dev>
    | | * | 217fea9 - refactored urlpath._clear_ancenstor_cache to use article.ancenstor_objects generator (3 years, 2 months ago) <tschmidt-dev>
    | | * |   7a2985c - merge (3 years, 2 months ago) <tschmidt-dev>
    | | |\ \  
    | | * | | e20b2d6 - clear ancestor cache on save and delete article so that things like article_lists are refreshed (3 years, 2 months ago) <tschmidt>
    | | | |/  
    | | |/|   
    * | | | 6641ed1 - use self.stdout in django_notify management script logging (see django docs: https://docs.djangoproject.com/en/dev/howto/custom-management-commands/) (3 years, 2 months ago) <benjaoming>
    |/ / /  
    * | | df27e51 - Fixed posting data to views.article.Preview (3 years, 2 months ago) <benjaoming>
    | |/  
    |/|   
    * | c775a18 - #111 Add ancestor generator to Article (3 years, 2 months ago) <benjaoming>
    |/  
    * 9ca892d - Do not use URLField, it does not allow relative paths (3 years, 2 months ago) <benjaoming>
    * 7ec137f - Redirect from sign up and login pages for logged in users. Use wiki:root url for root article. (3 years, 2 months ago) <benjaoming>
    * 0af4af2 - #119 restore if image deleted and uploading new image file (3 years, 2 months ago) <benjaoming>
    * b73278c - remove initial blank attachments and images (3 years, 2 months ago) <benjaoming>
    * 7f6acb7 - #119 do not fail when deleting blank image and attachment fields (3 years, 2 months ago) <benjaoming>
    * 51497ca - page title for signup page (3 years, 2 months ago) <benjaoming>
    *   c06108c - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 2 months ago) <benjaoming>
    |\  
    | *   c8eeab5 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 2 months ago) <benjaoming>
    | |\  
    * | \   6e9f4f5 - Add a simple honeypot for signups #116 (3 years, 2 months ago) <benjaoming>
    |\ \ \  
    | |/ /  
    |/| /   
    | |/    
    | * a570d0a - Add a simple honeypot for signups (3 years, 2 months ago) <benjaoming>
    * | acd9636 - Add a simple honeypot for signups #117 (3 years, 2 months ago) <benjaoming>
    |/  
    *   2173d4b - Merge pull request #117 from jdcaballero/master (3 years, 2 months ago) <benjaoming>
    |\  
    | * c96d656 - User creation form extendedto include email as a required field (3 years, 2 months ago) <Juan Diego Caballero>
    | *   3932d27 - Merge branch 'master' of https://github.com/benjaoming/django-wiki (3 years, 2 months ago) <Juan Diego Caballero>
    | |\  
    | * | f0b25a5 - UserCreateForm subclassed to include the email as a required parameter in the signup. (3 years, 2 months ago) <Juan Diego Caballero>
    * | | 80790d5 - #118 django 1.5 (3 years, 2 months ago) <benjaoming>
    * | | 3950de5 - Fix #118 Avoid deprecation warning in Django 1.5 (3 years, 2 months ago) <benjaoming>
    * | |   e091f01 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 2 months ago) <benjaoming>
    |\ \ \  
    | * | | c6f9ee5 - Fix #118 Avoid deprecation warning in Django 1.5 (3 years, 2 months ago) <benjaoming>
    * | | | 6367157 - Fix #118 (forgot django_notify) Avoid deprecation warning in Django 1.5 (3 years, 2 months ago) <benjaoming>
    |/ / /  
    * | | 098faa1 - Add note in pluginbase about use of Meta.app_label (3 years, 2 months ago) <benjaoming>
    * | | b20094c - Inherit from EmptyQuerySet (3 years, 2 months ago) <benjaoming>
    | |/  
    |/|   
    * | a4f9d3b - Few more readme changes (3 years, 2 months ago) <benjaoming>
    * | ead17b0 - Todo and readme updates (3 years, 2 months ago) <benjaoming>
    * |   65c882b - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 2 months ago) <benjaoming>
    |\ \  
    | |/  
    | * efb617e - Update to 0.0.17 (3 years, 2 months ago) <benjaoming>
    * | a7254ab - (tag: alpha/0.0.17) bump to 0.0.17 (3 years, 2 months ago) <benjaoming>
    |/  
    * bfec4e8 - rename command, cleanup code, add logging (3 years, 2 months ago) <benjaoming>
    * 15b02ae - ignore settings_local (3 years, 2 months ago) <benjaoming>
    * 1e9d5b5 - remove print stm (3 years, 2 months ago) <benjaoming>
    * bcddb0b - Support and contributions (3 years, 2 months ago) <benjaoming>
    * d913907 - Support and contributions (3 years, 2 months ago) <benjaoming>
    *   088c0fe - Merge pull request #115 from jdcaballero/master (3 years, 2 months ago) <benjaoming>
    |\  
    | * fbd75ae - Subject changed to a translated string, notification email changed to @example.com (3 years, 2 months ago) <Juan Diego Caballero>
    | * c13d97d -  Notifications Implementation: (3 years, 2 months ago) <Juan Diego Caballero>
    | * a47c6da - Revert "Email Notifications Implementation" (3 years, 2 months ago) <Juan Diego Caballero>
    | * 700bb6e - Email Notifications Implementation (3 years, 2 months ago) <Juan Diego Caballero>
    |/  
    * e448e2b - Replace Markdown toc extension and add improved version to macro package. (3 years, 3 months ago) <benjaoming>
    * 9655067 - bootstrap typography (3 years, 3 months ago) <benjaoming>
    * ea70181 - bootstrap typography and remove extra <li>s on article_list (3 years, 3 months ago) <benjaoming>
    * 61131d8 - (tag: alpha/0.0.16) bump to 0.0.16 (3 years, 3 months ago) <benjaoming>
    * d66234e - cache key should be from current revision (3 years, 3 months ago) <benjaoming>
    * 089dd2f - restore lost-and-found auto collection if subtrees are disconnected (3 years, 3 months ago) <benjaoming>
    * fa3c916 - soft linebreak after images to conserve preceeding headline elements (3 years, 3 months ago) <benjaoming>
    * db07ac2 - invalidate article cache when plugins are updated (3 years, 3 months ago) <benjaoming>
    * 1dd4788 - thumbnail styles (3 years, 3 months ago) <benjaoming>
    * db73b51 - redirect for delete view to parent (3 years, 3 months ago) <benjaoming>
    * dcf7e72 - fix article purging (3 years, 3 months ago) <benjaoming>
    * c57656a - only show active children in article_list (3 years, 3 months ago) <benjaoming>
    * 701e34b - show article titles instead of slugs in index view (3 years, 3 months ago) <benjaoming>
    * ea1b3ad - allow inline attachment tag (3 years, 3 months ago) <benjaoming>
    * fc94f67 - do not show deleted files in list, add separate restore menu item (3 years, 3 months ago) <benjaoming>
    * fc9efa6 - non-zip files fix for moderators and clean up a bit (3 years, 3 months ago) <benjaoming>
    * e85cbc6 - title for TOCs (3 years, 3 months ago) <benjaoming>
    * b0a6d6e - bootstrap styling (3 years, 3 months ago) <benjaoming>
    * dfb5693 - python 2.5 compatibility for zip archives (3 years, 3 months ago) <benjaoming>
    * 1b5b583 - zip file uploading and extracting for moderators (3 years, 3 months ago) <benjaoming>
    * 4f019e7 - raise 404 if plugin is missing (3 years, 3 months ago) <benjaoming>
    * 0cabdfb - refactor article view to use view.html template (3 years, 3 months ago) <benjaoming>
    * 0579521 - fix spam protection wrongly targetting moderators (3 years, 3 months ago) <benjaoming>
    * 44b1e2f - Make cache timeout configurable and remove erred block tags from render.html (3 years, 3 months ago) <benjaoming>
    * 0d092fa - improve resizable to properly fit nested iframes etc (3 years, 3 months ago) <benjaoming>
    * ecaccbd - add request context processor and check that config is OK (3 years, 3 months ago) <benjaoming>
    * 6a3c777 - resizable modals (3 years, 3 months ago) <benjaoming>
    * e4d0669 - add template assignment tag login_url (3 years, 3 months ago) <benjaoming>
    * 73af524 - broken boostrap-responsive build (3 years, 3 months ago) <benjaoming>
    * be19fdb - do not show deleted articles in article_list macro (3 years, 3 months ago) <benjaoming>
    *   6be1a3d - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 3 months ago) <benjaoming>
    |\  
    | * eb3bd0b - Update README.md (3 years, 3 months ago) <benjaoming>
    * | e6e0a84 - Add better info about licensing (3 years, 3 months ago) <benjaoming>
    |/  
    * d25da1c - (tag: alpha/0.0.15) Bump to 0.0.15 (3 years, 3 months ago) <benjaoming>
    * 51daba0 - add model chart in pdf to the build-sdist process (3 years, 3 months ago) <benjaoming>
    * e7c70fd - typo (3 years, 3 months ago) <benjaoming>
    * 89b64aa - modify build to clean up old egg dir and add back the MANIFEST.in symlink (3 years, 3 months ago) <benjaoming>
    * d568683 - python 2.5 support (3 years, 3 months ago) <benjaoming>
    * 2c39d15 - do not fail when removing images located in non-existing dirs (3 years, 3 months ago) <benjaoming>
    * 628b59c - image plugin thumbnail css (3 years, 3 months ago) <benjaoming>
    * 948580c - image plugin thumbnail css (3 years, 3 months ago) <benjaoming>
    * da15d5d - use LESS for stylesheets by extending twitter-bootstrap (3 years, 3 months ago) <benjaoming>
    * 76a3532 - rm dupe lines (3 years, 3 months ago) <benjaoming>
    * f0c3458 - footer clearfix (3 years, 3 months ago) <benjaoming>
    *   ece1239 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 3 months ago) <benjaoming>
    |\  
    | *   94e6035 - Merge pull request #108 from SacNaturalFoods/master (3 years, 3 months ago) <benjaoming>
    | |\  
    | | * 26c922b - removed overlooked debug print statements (3 years, 3 months ago) <tschmidt-dev>
    | | * 4d34e70 - fixed macro arg regex for args longer than 1 character (3 years, 3 months ago) <tschmidt-dev>
    | |/  
    * | abe7282 - unfinished generic markdown extension (3 years, 3 months ago) <benjaoming>
    * | 53205ac - fix setting article fk on reusable plugins for identifying permissions (3 years, 3 months ago) <benjaoming>
    |/  
    * 7e6da88 - (tag: alpha/0.0.14) Bump to 0.0.14 (3 years, 3 months ago) <benjaoming>
    * 67d8cf3 - Security fix, do not call eval on input (3 years, 3 months ago) <benjaoming>
    * d9d19f0 - fix python 2.5 unknown elementree method (3 years, 3 months ago) <benjaoming>
    * f9a46f1 - (tag: alpha/0.0.13) Note on python 2.5 and improve article list (3 years, 3 months ago) <benjaoming>
    * c4e855d - Update README.md (3 years, 3 months ago) <benjaoming>
    * 076ad8e - Python 2.5 support note (3 years, 3 months ago) <benjaoming>
    * 0106b6f - python 2.5 support (3 years, 3 months ago) <benjaoming>
    * b86be8c - (tag: alpha/0.0.12) version bump to 0.0.12 (3 years, 3 months ago) <benjaoming>
    * d5f8352 - Fix #100 add print CSS and remove inline <style> (3 years, 3 months ago) <benjaoming>
    * 9070358 - Fix error in macros removing unknown tags from stack and prettify styling (3 years, 3 months ago) <benjaoming>
    * ff9ad26 - add a few more default markdown plugins (3 years, 3 months ago) <benjaoming>
    * 2ed231a - Apply user info on the creater of the first revision of the root article (3 years, 3 months ago) <benjaoming>
    * c50e05f - Display a helping exception message when MPTT is failing (3 years, 3 months ago) <benjaoming>
    * e25b3a4 - logo block for footer (3 years, 3 months ago) <benjaoming>
    * 1b06fb0 - Fix example code (3 years, 3 months ago) <benjaoming>
    * 2aabc2d - move macros configuration and do not include django_notify twice in the urlconf (3 years, 3 months ago) <benjaoming>
    * affa159 - Make django notify admin configurable so it can be excluded (3 years, 3 months ago) <benjaoming>
    *   d004700 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 3 months ago) <benjaoming>
    |\  
    | *   365793d - Merge pull request #107 from SacNaturalFoods/master (3 years, 3 months ago) <benjaoming>
    | |\  
    | | * 22486f5 - added kwargs logic to macros plugin and depth kwarg to article_list macro (3 years, 3 months ago) <tschmidt-dev>
    | |/  
    * | b336586 - Add help sidebar for macros and make allowed methods configurable (3 years, 3 months ago) <benjaoming>
    |/  
    * 0751cc8 - using wrong class for widget when in readonly mode on some settings form fields (3 years, 3 months ago) <benjaoming>
    * 86ee414 - receive post_save signal only using kwargs (3 years, 3 months ago) <benjaoming>
    * 91076f2 - security fix for macro plugin, add plugins.acros to testproject (3 years, 3 months ago) <benjaoming>
    *   933ac19 - Merge pull request #105 from SacNaturalFoods/master (3 years, 3 months ago) <benjaoming>
    |\  
    | * d6f3724 - restructured url resolver in article_list macro (3 years, 3 months ago) <tschmidt-dev>
    | * c0d5f25 - fixed article_list macro sublist markup (3 years, 3 months ago) <tschmidt-dev>
    | * a7bbf18 - added Django 1.5 url syntax to macros plugin; added condition to avoid generating empty lists for each child in article_list macro (3 years, 3 months ago) <tschmidt-dev>
    | * 5eda878 - added wiki-article-sublist class to article_list macro template (3 years, 3 months ago) <tschmidt-dev>
    | * 3493af1 - added wiki-article-list class to article_list macro template (3 years, 3 months ago) <tschmidt-dev>
    | * 5a3c029 - added core macros plugin with initial article_list macro (3 years, 3 months ago) <tschmidt-dev>
    * |   919d45e - Merge pull request #104 from SacNaturalFoods/master (3 years, 3 months ago) <benjaoming>
    |\ \  
    | |/  
    | * f14ecef - collapsed MARKDOWN_EXTENSIONS and MARKDOWN_SAFE_MODE settings into MARKDOWN_KWARGS (3 years, 3 months ago) <tschmidt-dev>
    * | f58974d - Update README.md (3 years, 3 months ago) <benjaoming>
    * | 4bf8769 - Update README.md (3 years, 3 months ago) <benjaoming>
    * |   61e5952 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 3 months ago) <benjaoming>
    |\ \  
    | * | 603898f - Update README.md (3 years, 3 months ago) <benjaoming>
    | * | 3167e4b - Update README.md (3 years, 3 months ago) <benjaoming>
    | * | 281e276 - Update README.md (3 years, 3 months ago) <benjaoming>
    * | | c93f3c5 - add debug_toolbar if installed (3 years, 3 months ago) <benjaoming>
    |/ /  
    * |   27f5b44 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 3 months ago) <benjaoming>
    |\ \  
    | * \   23f48b3 - Merge pull request #102 from SacNaturalFoods/master (3 years, 3 months ago) <benjaoming>
    | |\ \  
    | | |/  
    | | * 0f02092 - added MARKDOWN_SAFE_MODE setting (3 years, 3 months ago) <tschmidt-dev>
    | | * 8ac9814 - fixed help plugin TOC syntax and added Tables section (3 years, 3 months ago) <tschmidt-dev>
    | * |   31562fd - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 3 months ago) <benjaoming>
    | |\ \  
    * | | | 68fc90c - Add settings for inheriting owner and group permissions and fix #99 (3 years, 3 months ago) <benjaoming>
    * | | |   b1b3aea - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 3 months ago) <benjaoming>
    |\ \ \ \  
    | |/ / /  
    |/| / /   
    | |/ /    
    | * | c21775d - Use Form Media for SelectWidgetBootstrap and update wiki_form templatetag (3 years, 3 months ago) <benjaoming>
    | |/  
    * | 9c5f46d - Use Form Media for SelectWidgetBootstrap and update wiki_form templatetag Fix #95 (3 years, 3 months ago) <benjaoming>
    |/  
    * efd8db8 - WARNING! May break your config: Clean up settings variale names in images and attachments plugins and use unified defaults. Issue #91. (3 years, 4 months ago) <benjaoming>
    *   6b9f346 - Merge pull request #92 from gluwa/master (3 years, 4 months ago) <benjaoming>
    |\  
    | * 55a4a5b - in attachments plugin, append '.upload' to uploaded files only when settings.APPEND_EXTENSION is True. (3 years, 4 months ago) <Tae-lim Oh>
    | * 15a33ea - adding custom storage backend option to images plugin (3 years, 4 months ago) <Tae-lim Oh>
    |/  
    *   64a22a8 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 4 months ago) <benjaoming>
    |\  
    | * 5f90b18 - Update README.md (3 years, 4 months ago) <benjaoming>
    * | 453131e - add testproject template dir (3 years, 4 months ago) <benjaoming>
    * | 59567e3 - Error pages for test project (3 years, 4 months ago) <benjaoming>
    |/  
    * 9664ce1 - Add PIL to requirements.txt and remove Python 2.5 from travis (3 years, 4 months ago) <benjaoming>
    * 3607ea8 - test with manage.py (3 years, 4 months ago) <benjaoming>
    * 659d145 - fix double requirement (3 years, 4 months ago) <benjaoming>
    *   6c7f905 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 4 months ago) <benjaoming>
    |\  
    | * 62d2c4f - Update README.md (3 years, 4 months ago) <benjaoming>
    * | 558d88c - fix pip argument for travis (3 years, 4 months ago) <benjaoming>
    |/  
    * 3b2aceb - travis config added (3 years, 4 months ago) <benjaoming>
    * 09cab11 - missing template load stm (3 years, 4 months ago) <benjaoming>
    * c14ee73 - Use JS to save article form data on all sidebar plugin forms (3 years, 4 months ago) <benjaoming>
    * 2e36575 - Scroll if there are many images, only warn about unsaved changes if there are in fact such (3 years, 4 months ago) <benjaoming>
    * fb40d08 - Avoid losing user data when a sidebar form is called and article contents have been modified #33 (3 years, 4 months ago) <benjaoming>
    * b9e95ef - Support for I10N - use timezone.now (3 years, 4 months ago) <benjaoming>
    * ab45a20 - Cleanup nicely when an image or attachment is deleted - remove the file and any empty directories #25 (3 years, 4 months ago) <benjaoming>
    * 36eb1f8 - Do not allow merging with a deleted revision #27 (3 years, 4 months ago) <benjaoming>
    * 652433f - Remove unused setting (3 years, 4 months ago) <benjaoming>
    * 8a010d8 - apply migrations to prepopulated test database (3 years, 4 months ago) <benjaoming>
    * 6eb99d2 - Account handling system should pass all django.contrib.auth test cases #86 (3 years, 4 months ago) <benjaoming>
    * ea2cd01 - Account handling system should pass all django.contrib.auth test cases #86 (3 years, 4 months ago) <benjaoming>
    * df59145 - Redirect for the built-in account handling when login is required + better err page. (3 years, 4 months ago) <benjaoming>
    * c805fee - Add link to forum/mailing list (3 years, 4 months ago) <benjaoming>
    * ac826e3 - sorl.thumbnail in INSTALLED_APPS + copy-paste friendly (3 years, 4 months ago) <benjaoming>
    * e8dcb97 - Update README.md (3 years, 4 months ago) <benjaoming>
    * bde97a5 - Update README.md (3 years, 4 months ago) <benjaoming>
    * 97734d0 - Update README.md (3 years, 4 months ago) <benjaoming>
    * f482b0c - Bumping to version 0.0.9 for new PyPi release (3 years, 4 months ago) <benjaoming>
    * 3add660 - Remove 'center' from javascript prompt help text (#88) (3 years, 5 months ago) <benjaoming>
    * 2c0b35a - Add local settings to testproject (3 years, 6 months ago) <benjaoming>
    * 82b4e32 - #71 and #87 - put the 'get' by path pattern at the very end of all patterns (3 years, 6 months ago) <benjaoming>
    * 9604209 - #71 - missing pattern 'get' in new class based urls (3 years, 6 months ago) <benjaoming>
    *   a106977 - Merge pull request #85 from shaunc/master (3 years, 6 months ago) <benjaoming>
    |\  
    | * f0592f5 - fixes merge (3 years, 6 months ago) <Shaun Cutts>
    | *   9a38e27 - merges recent changes w/ classurl branch (3 years, 6 months ago) <Shaun Cutts>
    | |\  
    |/ /  
    | * f8900d0 - adds class for url configuration (3 years, 6 months ago) <Shaun Cutts>
    | * 5e812ac - updates {% url %} use in notifications menubaritem template to confrom to django 1.5 (3 years, 6 months ago) <Shaun Cutts>
    * | c93b318 - Be explicit about application order (#84) (3 years, 6 months ago) <benjaoming>
    * |   ceb705b - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 6 months ago) <benjaoming>
    |\ \  
    | * | 6704790 - Retry: Fix settings.py link (#81) (3 years, 6 months ago) <benjaoming>
    | * | f84a092 - Fix settings.py link (#81) (3 years, 6 months ago) <benjaoming>
    | * | d586040 - Fix settings.py link (3 years, 6 months ago) <benjaoming>
    * | | 32591c2 - Regression from adding spam protection, missing argument in when view class Preview initialized EditForm (#83) (3 years, 6 months ago) <benjaoming>
    |/ /  
    * | 2cb3950 - Move all javascript to load at the bottom of the page and ensure only to add javascript inside Sekizai addtoblock tag. (#54) (3 years, 6 months ago) <benjaoming>
    * | 109421e - Fix markdown extension for images to allow no align:xx specified and use bootstrap pull-left and pull-right. Don't allow center alignment. (#65) (3 years, 6 months ago) <benjaoming>
    * | 1834071 - Add spam/bot protection by verifying user session and ip_address and check the number of recent revisions (#72) Add global setting to disable anonymous article creation (#72) (3 years, 6 months ago) <benjaoming>
    * | ecbacc8 - Count number of occurences of the same message and display "x times" in the notification list instead of duplicate messages. (3 years, 6 months ago) <benjaoming>
    * | ea71c5c - Add warning on Edit page if user is not logged in w/ link to login page and redirect back to edit page (#55) (3 years, 6 months ago) <benjaoming>
    * | 58cb725 - eh..remove alert() (3 years, 6 months ago) <benjaoming>
    * | ce1ff2e - Setting Colorbox.js width and height (#69) and adding captions. (3 years, 6 months ago) <benjaoming>
    * |   2458217 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 6 months ago) <benjaoming>
    |\ \  
    | * | cb3d251 - Ensure that CreateForm fails when slug field is longer than the maximum allowed slug length (#54). (3 years, 6 months ago) <benjaoming>
    * | | 1dbd51f - Ensure that CreateForm fails when slug field is longer than the maximum allowed slug length (#57) (3 years, 6 months ago) <benjaoming>
    |/ /  
    * | 393aa34 - Adding check on article locked for attachments. (#74) - Also cleaning up attachment list and removing forms when article is locked. Adding template filter is_locked (3 years, 6 months ago) <benjaoming>
    * | 9d801fb - Adding Bootstrap 2.2.0 (3 years, 6 months ago) <benjaoming>
    * |   e948b73 - Merge pull request #79 from avtobiff/update-readme-dependencies (3 years, 6 months ago) <benjaoming>
    |\ \  
    | * | f31b6d4 - Correct django dependency invariant (3 years, 6 months ago) <Per Andersson>
    | * | 78fa3a8 - Increase django-mptt dependency version (3 years, 6 months ago) <Per Andersson>
    |/ /  
    * |   f3f667e - Merge pull request #75 from jdcaballero/master (3 years, 6 months ago) <benjaoming>
    |\ \  
    | * | 0f422c0 - Update wiki/plugins/notifications/forms.py (3 years, 6 months ago) <jdcaballero>
    |/ /  
    * | e7d64e1 - Never return a proxy object from __unicode__ ! (#73) (3 years, 6 months ago) <benjaoming>
    * |   46fc152 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 6 months ago) <benjaoming>
    |\ \  
    | |/  
    | *   2288efd - Merge pull request #64 from webdevelop/master (3 years, 7 months ago) <benjaoming>
    | |\  
    | | * d77930c - Greedy regex algorithm (3 years, 7 months ago) <Vladyslav>
    * | | a479748 - Never return a proxy object from __unicode__ ! (#73) (3 years, 6 months ago) <benjaoming>
    |/ /  
    * | 0c8a554 - Issue #68 - Add sorl-thumbnail to dependencies. Furthermore, add >=0.5.3 to django-mptt which has caused some reports. Read requirements.txt into setup.py to avoid hard coding and mismatches. Create 0.0.2 release which is not broken because README.md was missing from distribution file. (3 years, 7 months ago) <benjaoming>
    * | 5db399c - Issue #67 - left joins caused by m2m fields sometimes result in duplicate rows, applying distinct() (3 years, 7 months ago) <benjaoming>
    * | 0850915 - Fix Issue #66 (3 years, 7 months ago) <benjaoming>
    * | d08301f - Fix transaction support for uploading attachments (3 years, 7 months ago) <benjaoming>
    * | ee08a7f - Fix #60 - do not allow empty image form fields even though the model should handle it. (3 years, 7 months ago) <benjaoming>
    * | 520e123 - Fixing long titles in notifications and display total count of notifications instead of just a truncated number. (3 years, 7 months ago) <benjaoming>
    * | a886040 - Cosmetic changes to fix #38 - but otherwise there is no rules for URL lengths other than IE setting the lower limit at 2048 characters which should hardly annoy anyone. (3 years, 7 months ago) <benjaoming>
    * | 8884709 - Remove redundant table (3 years, 7 months ago) <benjaoming>
    * | bbd4234 - Issue#50 - make using send_file configurable to allow for remote storage backends such as S3. (3 years, 7 months ago) <benjaoming>
    * |   1082aef - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 7 months ago) <benjaoming>
    |\ \  
    | * | 0bc5611 - Update README.md (3 years, 7 months ago) <benjaoming>
    | * |   4e2ced2 - Merge pull request #62 from webdevelop/master (3 years, 7 months ago) <benjaoming>
    | |\ \  
    | | |/  
    | | * e0a3b99 - Uncode filename in US-ASCII format, needable for russian and other language (3 years, 8 months ago) <Vladyslav>
    | | * f723c60 - Change max_length of file to 255 for handling files with big name (3 years, 8 months ago) <Vladyslav>
    | * | 9e3a9d0 - Adding news section about RC1. (3 years, 7 months ago) <benjaoming>
    | |/  
    | *   4f750cd - Merge pull request #52 from pypetey/master (3 years, 8 months ago) <benjaoming>
    | |\  
    | | * 0fd815b - small fix for extra hash (3 years, 8 months ago) <pypetey>
    | | * 3183706 - Fix for line 561 error: 'msgid' format string with unnamed arguments cannot be properly localized: The translator cannot reorder the arguments. Please consider using a format string with named arguments, and a mapping instead of a tuple for the arguments. (3 years, 8 months ago) <pypetey>
    | |/  
    * | 2a9167a - Add support for counting duplicate notifications instead of repeating the same. (3 years, 7 months ago) <benjaoming>
    |/  
    * 0fa8bad - Use safe preprocessors for attachments and images plugin. Fix Issue #39. Also use a template to render attachments html. (3 years, 8 months ago) <benjaoming>
    * 8d1dd37 - Updating model chart to reflect current project status (3 years, 8 months ago) <benjaoming>
    * 9503fac - Issue #50 do not use full paths because remote storage does not implement this. (3 years, 8 months ago) <benjaoming>
    * 8f64202 - Issue #48: Searches should be case insensitive (3 years, 8 months ago) <benjaoming>
    * b68f0b5 - More modifications for pypi, first 0.0.1 released - pip install wiki (3 years, 8 months ago) <benjaoming>
    * 996800c - Adding a MANIFEST for pypi distribution (3 years, 8 months ago) <benjaoming>
    * da4e421 - Fixing issues with PYPI compatibility (3 years, 8 months ago) <benjaoming>
    *   8a589bb - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 8 months ago) <benjaoming>
    |\  
    | *   c7aa2e1 - Merge pull request #40 from uAnywhere/master (3 years, 8 months ago) <benjaoming>
    | |\  
    | | * 4e6cdda - Minor optimisation to ACLs (use .exists() instead of bool() because it's faster), fix an issue on Django 1.5 where EmptyQuerySet has no method select_related_common() (3 years, 8 months ago) <Michael Farrell>
    | |/  
    * | 3a31f2c - Do not conditionally include login, logout and signup URLs in urlpatterns. Handle WIKI_ACCOUNT_HANDLING inside views. Issue #43. (3 years, 8 months ago) <benjaoming>
    |/  
    *   76b0698 - Merge branch 'edx_release' (3 years, 8 months ago) <benjaoming>
    |\  
    | * 7fad1ac - (origin/edx_release) Removing settings from links plugin (3 years, 8 months ago) <benjaoming>
    | * d489d13 - Merging with edx branch, fixing link plugin to not use live_lookups (it's meaningless because whole articles are normally cached and therefore, links are not resolved at every article view). Also, settings for the links plugin were wrongly placed in the main settings file. (3 years, 8 months ago) <benjaoming>
    | *   72faa3b - Merge pull request #31 from rocha/edx_release (3 years, 8 months ago) <benjaoming>
    | |\  
    | | * cd1c23e - Fixed WikiPath regexp. It was incorrectly matching [Title](Link) on the same line. (3 years, 8 months ago) <Carlos Andrés Rocha>
    | |/  
    | * 7e42bce - Changed behavior of wikilinks extension to optionally disable database and prefer to stay at a certain level. (3 years, 8 months ago) <Bridger Maxwell>
    | * f00b7d3 - Fixed bug where non-found wiki links ignored base url. (3 years, 8 months ago) <Bridger Maxwell>
    | * 533c7fc - Dir links are now prominently view links with arrows for viewing children. (3 years, 8 months ago) <Bridger Maxwell>
    | * d1b97e2 - Fixed bug for calling .active() on empty query sets. (3 years, 8 months ago) <Bridger Maxwell>
    | * 50c08a3 - Added setting for disabling SelectWidgetBootstrap. (3 years, 8 months ago) <Bridger Maxwell>
    | * 3576a2d - Allowing periods in slug for wikilinks. (3 years, 8 months ago) <Bridger Maxwell>
    * |   81bf613 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 8 months ago) <benjaoming>
    |\ \  
    | * | 7aab68a - Adding ideas section. (3 years, 8 months ago) <benjaoming>
    * | | bb87802 - unchanged, git detects change but shows no diff (3 years, 8 months ago) <benjaoming>
    * | | 0fc9b2d - Important fix! Remove HTML tags from Markdown code. (3 years, 8 months ago) <benjaoming>
    * | | 4a58ac1 - Adding clearfix (3 years, 8 months ago) <benjaoming>
    |/ /  
    * | 98aaee3 - Issue #32, yes, clearly a typo here. Don't know why it was working, but replaced with super(RevisionForm.. and tested. (3 years, 8 months ago) <benjaoming>
    * |   7435980 - Merge pull request #35 from rfurman/master (3 years, 8 months ago) <benjaoming>
    |\ \  
    | * | 60142fa - Fixed image captions by resetting caption_lines for each new image.  Before, the n-th image would have the first n captions concatenated together. (3 years, 8 months ago) <Ralph Furmaniak>
    |/ /  
    * |   60c83ee - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 8 months ago) <Bridger Maxwell>
    |\ \  
    | * | d9518ea - Only mark shown notifications as read -- never the ones that haven't been display because only 10 notifications are display at the same time... (3 years, 8 months ago) <benjaoming>
    | * | ebfaff4 - order notifications (3 years, 8 months ago) <benjaoming>
    | * | e229819 - Notify dropdown should look at the latest id of a notification and not retrieve any older notifications on updating from JSON. (3 years, 8 months ago) <benjaoming>
    | * | 288e25a - Merge user menu and notifications menu (3 years, 8 months ago) <benjaoming>
    | * | 3c9c2f1 - more search layout (3 years, 8 months ago) <benjaoming>
    | * |   6d20678 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 8 months ago) <benjaoming>
    | |\ \  
    | * | | f8a6e1c - Search "optimization".... layout-wise :) (3 years, 8 months ago) <benjaoming>
    * | | | a558ea6 - Allowing periods in slug for wikilinks. (3 years, 8 months ago) <Bridger Maxwell>
    | |/ /  
    |/| |   
    * | | 7f820b6 - user.is_superuser is not a function. (3 years, 8 months ago) <Bridger Maxwell>
    |/ /  
    * |   0012481 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 8 months ago) <benjaoming>
    |\ \  
    | |/  
    | * 63003aa - Removed print statement accidentally left in. (3 years, 8 months ago) <Bridger Maxwell>
    | * afdd97d - Made a workaround for django bug 15040, which made permissions forms have all checked boxes. (3 years, 8 months ago) <Bridger Maxwell>
    | * 6ccd08e - Moved subtree delete to a model method with transactions. (3 years, 8 months ago) <Bridger Maxwell>
    * | c0d7e2a - Search function (3 years, 8 months ago) <benjaoming>
    |/  
    * c2cfcc2 - A few search related things... adding search bar (doesnt work yet) (3 years, 8 months ago) <benjaoming>
    * 56d8e57 - Filtering on Directory listings. Issue #27 - never create a merged revision that inherits the deleted or locked attribute. (3 years, 8 months ago) <benjaoming>
    * 2979c98 - Few things here and there in the README (3 years, 8 months ago) <benjaoming>
    * ff8fd1c - Issue #28 (3 years, 8 months ago) <benjaoming>
    *   bf0d9cd - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 8 months ago) <benjaoming>
    |\  
    | * 9865b5c - Changed preview to show warning when previewing a deleted revision. (3 years, 8 months ago) <Bridger Maxwell>
    | * d2f08a3 - You can now preview deleted revisions (so they work in the history tab). (3 years, 8 months ago) <Bridger Maxwell>
    | * a8dbb5f - Fixed confusing if statement that had the side effect of restoring every deleted article a moderator views. (3 years, 8 months ago) <Bridger Maxwell>
    | *   c432574 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 8 months ago) <Bridger Maxwell>
    | |\  
    | * | 1415c85 - Was accidentally using old permission for showing purge confirm form. (3 years, 8 months ago) <Bridger Maxwell>
    * | | b03a317 - Very small commit before merge... (3 years, 8 months ago) <benjaoming>
    * | | 8e691c1 - Modal should not animate... the bootstrap animation is loo choppy (3 years, 8 months ago) <benjaoming>
    | |/  
    |/|   
    * |   6be6a0c - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 8 months ago) <benjaoming>
    |\ \  
    | |/  
    | *   32416cd - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 8 months ago) <Bridger Maxwell>
    | |\  
    | * | ce4fd7a - Removed the lost and found until it can be debugged. (3 years, 8 months ago) <Bridger Maxwell>
    | * | 4ddc7cb - Properly deletes children when purging articles. (3 years, 8 months ago) <Bridger Maxwell>
    | * |   632bb59 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 8 months ago) <Bridger Maxwell>
    | |\ \  
    | * \ \   096e149 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 8 months ago) <Bridger Maxwell>
    | |\ \ \  
    | * \ \ \   af0b2a6 - Merge branch 'edx_release' (3 years, 8 months ago) <Bridger Maxwell>
    | |\ \ \ \  
    | | * | | | 82806fa - An article is now considered deleted if a parent is instead of explicitly needing to mark all children as deleted. (3 years, 8 months ago) <Bridger Maxwell>
    | | * | | | 02275fb - Fixed import for installation to run without attachments being enabled. (3 years, 8 months ago) <Bridger Maxwell>
    * | | | | | 915260d - oops mess (3 years, 8 months ago) <benjaoming>
    | |_|_|_|/  
    |/| | | |   
    * | | | | 59ecabd - Layout stuff (3 years, 8 months ago) <benjaoming>
    * | | | | 2770ad1 - Fix slug checking: Should respect case sensitivity (if configured) and feedback if its a deleted article (3 years, 8 months ago) <benjaoming>
    | |_|_|/  
    |/| | |   
    * | | | 66f357e - Removing the stupid delete check once and for all (3 years, 8 months ago) <benjaoming>
    | |_|/  
    |/| |   
    * | | d5d90a4 - Removing circular permission check can_write->can_delete->can_write.... (3 years, 8 months ago) <benjaoming>
    * | | a3ee89d - Adding user_can_read as a kwarg on Article.get_children (3 years, 8 months ago) <benjaoming>
    |/ /  
    * | 489dcba - Removing the is_moderator decorator -- it is replaced by can_moderate (3 years, 8 months ago) <benjaoming>
    * | 9a996a7 - Updating todo and comments (3 years, 8 months ago) <benjaoming>
    * |   1e5bb80 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 8 months ago) <benjaoming>
    |\ \  
    | * \   221fca1 - Merge branch 'edx_release' (3 years, 8 months ago) <Bridger Maxwell>
    | |\ \  
    | | |/  
    | | * 876357a - Added an error page (for when even the parent isn't found). (3 years, 8 months ago) <Bridger Maxwell>
    * | | 832d790 - Loads of changes in permission system. Many aspects are now configurable. (3 years, 8 months ago) <benjaoming>
    |/ /  
    * | 495d70e - Adding a couple of new settings that are not fully implemented yet. Do not let MARKDOWN_EXTENSIONS be a callable since the markdown_instance already has an article property accessible to any extension that wants it. (3 years, 8 months ago) <benjaoming>
    * | 9392b2f - Image deletion: Purge function to throw out files and everything! (3 years, 8 months ago) <benjaoming>
    * | 72a2884 - Update TODO. Should allow null values of image width and height since image files disappear sometimes and fields have to be emptied. (3 years, 8 months ago) <benjaoming>
    * | 46c4857 - Image captions should keep line breaks. Missing image files still keep causing problems (3 years, 8 months ago) <benjaoming>
    * | 5b49a60 - Fix whitespaces added from html template (3 years, 8 months ago) <benjaoming>
    * | 5352792 - Locking of articles and source view. (3 years, 8 months ago) <benjaoming>
    * | 8b4f51b - Settings tab should inherit from article.html (3 years, 8 months ago) <benjaoming>
    * | 4d941f6 - View Source is almost finished... (3 years, 8 months ago) <benjaoming>
    * | 4287c93 - Updates relating to new bootstrap version. Removing several js plugins as they are now in the minified bootstrap.js (3 years, 8 months ago) <benjaoming>
    * | 65147c5 - Inherit correct properties from predecessor and be more robust when returning size and filename on images (3 years, 8 months ago) <benjaoming>
    * | 657831f - IOError, not OSError (3 years, 8 months ago) <benjaoming>
    * | fabea44 - Add image.null=True for images field so that files can disappear and not cause unreparable error. (3 years, 8 months ago) <benjaoming>
    * | 471f8eb - Image replacement bug, did not inherit from predecessor (3 years, 8 months ago) <benjaoming>
    * | bff93ef - Updating test database (3 years, 8 months ago) <benjaoming>
    * | b4c18cb - Update to Bootstrap 2.1.0 (3 years, 8 months ago) <benjaoming>
    * | b39f8f1 - Printer friendliness (3 years, 9 months ago) <benjaoming>
    * | f9130a6 - Various small fixes (3 years, 9 months ago) <benjaoming>
    * | 1a4ef5a - Add links plugin to testproject. Do not fail if an attachment file has disappeared. (3 years, 9 months ago) <benjaoming>
    * | 2b8c7f4 - Adding a plugin for handling links and detecting if they are broken (which will show a read link in the article text). Also a sidebar for looking up links with typeahead. (3 years, 9 months ago) <benjaoming>
    |/  
    * e237b2a - Creating a proper WikiSlug javascript generator from the django urlify (3 years, 9 months ago) <benjaoming>
    *   95d8651 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 9 months ago) <benjaoming>
    |\  
    | * a49b4d5 - Patch for django bug where EmptyQuerySet actually needs the model to be set (or it can't raise a DoesNotExist exception). (3 years, 9 months ago) <Bridger Maxwell>
    * | 354c6b2 - Customizable storage backend for attachments. Proper error handling for illegal file types on replace view. (3 years, 9 months ago) <benjaoming>
    |/  
    * 7216584 - Browsing levels and adding articles to either current or parent level so users dont get confused about the hierarchy (3 years, 9 months ago) <benjaoming>
    * c83ad43 - Checking read permissions on page list (3 years, 9 months ago) <benjaoming>
    * b37e140 - Move add_select_related so it isn't a class method but an instance method of the URLPath's querysets. Fix error in permission lookup of users in a group. (3 years, 9 months ago) <benjaoming>
    * 0a273ee - Forgot a file in last commit, list.html (3 years, 9 months ago) <Bridger Maxwell>
    *   92ab132 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 9 months ago) <Bridger Maxwell>
    |\  
    | * 5988130 - Sidebar to handle plugins without a form (3 years, 9 months ago) <benjaoming>
    | * cd60dfd - Removing after refactor (3 years, 9 months ago) <benjaoming>
    | * 8d7f606 - Adding a help plugin and extra markdown extensions (3 years, 9 months ago) <benjaoming>
    | * 1b69061 - Permissions in settings tab can be applied recursively and owner can be changed. (3 years, 9 months ago) <benjaoming>
    | *   85c58dc - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 9 months ago) <benjaoming>
    | |\  
    | * | 3edd286 - Adding possibility for Plugins to add media to rendering pages. Adding advanced markdown extension for images. Adding colorbox for images plugin to enlarge photos. (3 years, 9 months ago) <benjaoming>
    * | | 2edd8d3 - Added simple child list page. Doesn't have any styling yet. (3 years, 9 months ago) <Bridger Maxwell>
    | |/  
    |/|   
    * | 2d7c987 - children_slice is no longer queried when SHOW_MAX_CHILDREN=0 (3 years, 9 months ago) <Bridger Maxwell>
    * | 55469f7 - Further reducing sql queries. (3 years, 9 months ago) <Bridger Maxwell>
    * | 7c6af7b - Added caching of ancestors for urlpath to reduce sql queries. (3 years, 9 months ago) <Bridger Maxwell>
    |/  
    * df4fd06 - Sending request object to sidebar forms (3 years, 9 months ago) <benjaoming>
    * 7c1542c - Adding new image revisions and better looks for history page (3 years, 9 months ago) <benjaoming>
    * fcc466d - Image management, revert, delete and restore (3 years, 9 months ago) <benjaoming>
    * c145596 - Refactoring wiki.core.plugins (3 years, 9 months ago) <benjaoming>
    *   ebe86a4 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 9 months ago) <benjaoming>
    |\  
    | * 97f8413 - Fixed some circular imports that were causing errors. (3 years, 9 months ago) <Bridger Maxwell>
    | * 8e76eae - IMPORTANT: Fix this. I just commented out a line that was causing trouble. (3 years, 9 months ago) <Bridger Maxwell>
    | * 96328e3 - Changed getting of EditorClass and editor to functions (so they don't run so early). (3 years, 9 months ago) <Bridger Maxwell>
    * | 45b67b2 - Adding RevisionPlugin. Images plugin becoming a plugin with its own revision system. Fixing anonymous settings for attachments plugin. (3 years, 9 months ago) <benjaoming>
    |/  
    *   d58dcbc - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 9 months ago) <Bridger Maxwell>
    |\  
    | * 1438944 - Moving sidebar outside of the main edit form so plugins can handle their own form data independently (3 years, 9 months ago) <benjaoming>
    * | 0072871 - Removed debug print. (3 years, 9 months ago) <Bridger Maxwell>
    |/  
    * eea5726 - Changing plugin base models for a more intuitive understanding of what types of models should exist. The image model should maintain revisions of itself to avoid a difficult process when replacing images. (3 years, 9 months ago) <benjaoming>
    * d4de685 - admin.py uses correct import of Editor, EditorClass. (3 years, 9 months ago) <Bridger Maxwell>
    * 12cc515 - Creating editors package with markitup module (3 years, 9 months ago) <benjaoming>
    * 8a7a3e7 - New app label for notifications (3 years, 9 months ago) <benjaoming>
    *   63b6da7 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 9 months ago) <benjaoming>
    |\  
    | * 95dd8fe - Moved MarkItUp editors to plugins also. (3 years, 9 months ago) <Bridger Maxwell>
    * | 8c84848 - comments (3 years, 9 months ago) <benjaoming>
    * | a4ef195 - New tables after altering APP_LABEL on plugins (3 years, 9 months ago) <benjaoming>
    |/  
    * d567a4d - Moving BaseEditor to wiki.plugins to avoid circular imports (3 years, 9 months ago) <benjaoming>
    *   944075a - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 9 months ago) <benjaoming>
    |\  
    | * 48a1377 - Fixed render_to_string parameter (context was being passed in without using 'context_instance' kwarg) (3 years, 9 months ago) <Bridger Maxwell>
    | *   7b6078b - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 9 months ago) <Bridger Maxwell>
    | |\  
    | * | 7ec4943 - Small typo where I used ANONYMOUS instead of ANONYMOUS_WRITE. (3 years, 9 months ago) <Bridger Maxwell>
    * | | 9a04ef4 - Changing app_label for plugin models (3 years, 9 months ago) <benjaoming>
    | |/  
    |/|   
    * | ab7dc9a - Adding migrations for URLPath.article cache field Adding dependency on sorl-thumbnail (3 years, 9 months ago) <benjaoming>
    * |   3e7ddf6 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 9 months ago) <benjaoming>
    |\ \  
    | |/  
    | * 473fd5e - Added a permission denied page. (3 years, 9 months ago) <Bridger Maxwell>
    | * 3324ab0 - Added a permission denied page. (3 years, 9 months ago) <Bridger Maxwell>
    * | 1d3677b - prefetch and swap lookups such that path is always looked up before article_id (3 years, 9 months ago) <benjaoming>
    * |   6af3dcb - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 9 months ago) <benjaoming>
    |\ \  
    | |/  
    | * 8cd2bb7 - ANONYMOUS and ANONYMOUS_WRITE settings are now respected. (3 years, 9 months ago) <Bridger Maxwell>
    | * 9c83dfb - Fixed issues where 'if user.is_anonymous' was missing () so was always True (3 years, 9 months ago) <Bridger Maxwell>
    | * 484ff1c - Added auto migration. (3 years, 9 months ago) <Bridger Maxwell>
    | * cdb2c3a - Added a bit of caching to retrieving path, so it doesn't make so many sql queries. (3 years, 9 months ago) <Bridger Maxwell>
    | * 6c9e1a0 - Added a hack to the hacky reverse to allow for transforms on reversed url. (3 years, 9 months ago) <Bridger Maxwell>
    * | 5fe706c - Merging with Basecamp feature list (3 years, 9 months ago) <benjaoming>
    |/  
    *   4ab9701 - Merge branch 'master' of git://github.com/benjaoming/django-wiki (3 years, 9 months ago) <Bridger Maxwell>
    |\  
    | * b85791d - Message after uploading image. Do not redirect after plugin form submit as changes to article text and title are lost. (3 years, 9 months ago) <benjaoming>
    | * 0863c41 - Sidebar plugins. First plugin: images. Upload an image directly via a plugin on the edit page. (3 years, 9 months ago) <benjaoming>
    | * 6eae1fc - Instructions about settings and tips (3 years, 9 months ago) <benjaoming>
    | * 3a876d9 - Block anonymous access to upload files (3 years, 9 months ago) <benjaoming>
    * | c053503 - Added login_required to create_root. (3 years, 9 months ago) <Bridger Maxwell>
    * |   d238020 - Merge branch 'master' of git://github.com/benjaoming/django-wiki (3 years, 9 months ago) <Bridger Maxwell>
    |\ \  
    | |/  
    | * d1f50d1 - test db not properly synced (3 years, 9 months ago) <benjaoming>
    | * 19716f7 - Adding South migrations for wiki, django_notify and wiki plugins (3 years, 9 months ago) <benjaoming>
    | * a1d6ebe - Refactor plugins: Put base classes in wiki.plugins (3 years, 9 months ago) <benjaoming>
    | * f7f6527 - Deleted article view with purge and restore options (3 years, 9 months ago) <benjaoming>
    | * 63c7e9f - Correctly inform user that a deletion ALSO deletes children. (3 years, 9 months ago) <benjaoming>
    | * 8ce2236 - Deletion for articles: Soft delete and purge. Also soft deletes or purges children. A soft deletion creates a new revision in which the article is marked as deleted. (3 years, 9 months ago) <benjaoming>
    | * c1514ab - Do not delete old notifications when user unsubscribes + allow notifications to be created without a subscription (to enable notifications for only one specific user) (3 years, 9 months ago) <benjaoming>
    | * 4800d5b - Decorator for muting notifications + Issue #11 fix (3 years, 9 months ago) <benjaoming>
    | * 2eae064 - Correcting errors caused by removal of Article.title field. Almost done with Delete view. (3 years, 9 months ago) <benjaoming>
    * | c10ee82 - Corrected parameters on render_to_response. Also fixed login url resolution when ACCOUNT_HANDLING=False. (3 years, 9 months ago) <Bridger Maxwell>
    * |   9f1b3a9 - Merge branch 'master' of git://github.com/benjaoming/django-wiki (3 years, 9 months ago) <Bridger Maxwell>
    |\ \  
    | |/  
    | * c3303e1 - Example urlpattern Issue #12 (3 years, 9 months ago) <benjaoming>
    | * 84d44da - Updating week and date (3 years, 9 months ago) <benjaoming>
    | * 0303bcd - Headlines (3 years, 9 months ago) <benjaoming>
    | * 0de3382 - Nicer headlines for install instructions (3 years, 9 months ago) <benjaoming>
    | * 5710402 - Small things (3 years, 9 months ago) <benjaoming>
    | * 11b00ec - Adding mptt to requirements Issue #10 (3 years, 9 months ago) <benjaoming>
    | * 869a62e - Better install instructions for Issue #14 and #12 (3 years, 9 months ago) <benjaoming>
    | *   43c32df - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 9 months ago) <benjaoming>
    | |\  
    | | *   1888ff6 - Merge pull request #15 from hgdeoro/updates-on-readme (3 years, 9 months ago) <benjaoming>
    | | |\  
    | | | * 212b3a2 - Updated install instructions on README. (3 years, 9 months ago) <Horacio G. de Oro>
    | | * |   f365669 - Merge pull request #10 from hgdeoro/pip-requirements (3 years, 9 months ago) <benjaoming>
    | | |\ \  
    | | | * | 0b054e0 - README: added instructions: how to use requirements.txt to install dependencies. (3 years, 9 months ago) <Horacio G. de Oro>
    | | | * | 5e5640f - Creates a requirements.txt to facilitate installing dependencies. (3 years, 9 months ago) <Horacio G. de Oro>
    | | | |/  
    | * | | 94a3ebf - Remove redundant Article.title field (3 years, 9 months ago) <benjaoming>
    | * | | 4418482 - Making footer prettier, clean up code (3 years, 9 months ago) <benjaoming>
    | |/ /  
    * | |   341db91 - Merge branch 'master' of git://github.com/benjaoming/django-wiki (3 years, 9 months ago) <Bridger Maxwell>
    |\ \ \  
    | |/ /  
    | * | 846a665 - Cleaning up template boiler plate markup (3 years, 9 months ago) <benjaoming>
    | * | 588bcdd - Making notifications update in a smart way. Fixing wrong urls in accounts (3 years, 9 months ago) <benjaoming>
    | * | bf09bf4 - Changing the urlpatterns to always prioritize paths over IDs if a path string is supplied -- even an empty one for the root article. Also modifying models in pluginbase to not be abstract such that it is possible to generically access all types of plugins. (3 years, 9 months ago) <benjaoming>
    | * | 33186aa - Adding model chart generation of the wiki (3 years, 9 months ago) <benjaoming>
    | |/  
    * |   193d514 - Merge branch 'master' of git://github.com/benjaoming/django-wiki (3 years, 9 months ago) <Bridger Maxwell>
    |\ \  
    | |/  
    | * afce7d8 - msg when child menu is empty (3 years, 9 months ago) <benjaoming>
    | * b3bf535 - msg when child menu is empty (3 years, 9 months ago) <benjaoming>
    | * 1bff649 - insert transaction commits so they cover all cases (3 years, 9 months ago) <benjaoming>
    | * 7091ac9 - Use chained QuerySet objects for can_read and can_write methods and active() to filter out inactive objects. Issue #9 (3 years, 9 months ago) <benjaoming>
    * | a7a5f5e - Added related_name to Article.owner to prevent conflict with existing Simplewiki install. (3 years, 9 months ago) <Bridger Maxwell>
    |/  
    * ea26ab8 - Anonymous users cannot be used in queries! (3 years, 9 months ago) <benjaoming>
    * c619639 - Making more agile url patterns that are agnostic to either receiving a  path or an article_id. The path takes precedence over the article_id, except for the root article which needs to be forced in the template. Prettyfying the article revision list. (3 years, 9 months ago) <benjaoming>
    * 24ea671 - Failed use of select_related -- need some good idea. Better UI with current level's child articles as dropdown menu. (3 years, 9 months ago) <benjaoming>
    * 2864d69 - Avoid duplicate notifications for overlapping subscription types. Make notification list empty when marking all notifications as read. (3 years, 9 months ago) <benjaoming>
    * b676975 - Admin labels (3 years, 9 months ago) <benjaoming>
    * b232ea8 - Notifications for attachments plugin and plugins in general (3 years, 9 months ago) <benjaoming>
    * 276c658 - Prettyfying the attachments page (3 years, 9 months ago) <benjaoming>
    * c385fc6 - Renaming permission - no permissions should overlap in their meaning. Fixing can_read and can_write on Article instances to match new permissions. (3 years, 9 months ago) <benjaoming>
    * efe01f7 - Improving managers. Adding select_related (untested) on get_article decorator. Adding search function for attachments to add other article's attachments. Adding better permission handling through managers. (3 years, 9 months ago) <benjaoming>
    * 6988059 - Fixing preview function to use correct revision id (3 years, 9 months ago) <benjaoming>
    * 299017e - Wrong preview link (3 years, 9 months ago) <benjaoming>
    * 19b191a - Removing files that should not be in testproject (3 years, 9 months ago) <benjaoming>
    * d264f48 - Further frustations perhaps fixed on file upload issues (3 years, 9 months ago) <benjaoming>
    * 751c21a - Better error if permissions are wrong on MEDIA_ROOT (3 years, 9 months ago) <benjaoming>
    * b6e7b94 - Hopefully fixing transaction issue for other systems (3 years, 9 months ago) <benjaoming>
    * 0c57d76 - moving transaction commit (3 years, 9 months ago) <benjaoming>
    * 08bfb16 - More robustness in Attachments plugin. Give a good error message upon non-allowed uploads. Fix JSON decorator error. Ignore media files in test project. (3 years, 9 months ago) <benjaoming>
    * a2ba2c8 - Attachment plugin almost finished. Can delete and restore files and replace. Contains a smart obscurification feature that hides files. This way, files can have reading restrictions imposed. (3 years, 9 months ago) <benjaoming>
    * d96da78 - Better install instructions (3 years, 9 months ago) <benjaoming>
    * 81e8157 - Simple account handling, log in, log out and sign up. (3 years, 9 months ago) <benjaoming>
    * bfef21b - A bit of login toolbar (3 years, 9 months ago) <benjaoming>
    * ebb25ab - Adding notify frontend. (3 years, 9 months ago) <benjaoming>
    * 1a0396d - Adding from old feature list (3 years, 9 months ago) <benjaoming>
    * 5e3b668 - Add GPLv3 license, clean up code (3 years, 9 months ago) <benjaoming>
    * 8408f01 - More class-based views. Mixin class for Article-related views handling permissions etc. More complex plugin structure for easy creation of plugins with very easy integration in the article tab menu etc. (3 years, 9 months ago) <benjaoming>
    * fa4af85 - Error on saving revisions for anonymous users (3 years, 9 months ago) <benjaoming>
    * 64a20e8 - Adding notifications for article edits and creations (3 years, 9 months ago) <benjaoming>
    * 700e466 - Fixing js bug in SelectWidgetBootstrap (3 years, 9 months ago) <benjaoming>
    * 4162909 - Fix Issue #7 (in setup.py) + Add forms in settings tab, save new permissions and notification preferences (3 years, 9 months ago) <benjaoming>
    * 15a363d - Detection of editing conflicts, ie. concurrent article edits. If the revision number has changed while editing, warn the user and merge the user's content with the new revision. (3 years, 9 months ago) <benjaoming>
    * 9d92e96 - Updating the TODO (3 years, 9 months ago) <benjaoming>
    * 68e6c32 - added text editor backup files to gitignore; fix url tags so they are django 1.3-style, so it works properly with django 1.5 (which requires it) (3 years, 9 months ago) <Michael Farrell>
    * 3500999 - django_notify in wiki self-check on INSTALLED_APPS and a better README.md (3 years, 9 months ago) <benjaoming>
    * acff0fe - Update django_notify/README (3 years, 9 months ago) <benjaoming>
    * 083b56d - Update README.md (3 years, 9 months ago) <benjaoming>
    * 9dda155 - Update README.md (3 years, 9 months ago) <benjaoming>
    * 56ef8e6 - Update README.md (3 years, 9 months ago) <benjaoming>
    * 4ede9c8 - Creating new notification application django_notify and adding support for plugin registration and hooking additional forms into the settings page, such as notification settings for articles. (3 years, 9 months ago) <benjaoming>
    * 99041d5 - Redirecting if article does not exist, add user and ip_address to new articles (3 years, 9 months ago) <benjaoming>
    * efd542a - Create function added (3 years, 9 months ago) <benjaoming>
    * b75d893 - Diffs also display log messages and title changes (3 years, 9 months ago) <benjaoming>
    * 37b1cd5 - Pressing the final merge button now works and puts an automatic log entry (3 years, 9 months ago) <benjaoming>
    *   83394ad - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 9 months ago) <benjaoming>
    |\  
    | * 9360e1d - Update README.md (3 years, 9 months ago) <benjaoming>
    | * dc3e415 - Update README.md (3 years, 9 months ago) <benjaoming>
    * | e19ec3a - Viewing diffs and merging revisions. (3 years, 9 months ago) <benjaoming>
    |/  
    * 327ff0c - Issue #4 and #2 (3 years, 9 months ago) <benjaoming>
    *   06d06ce - Merge branch 'master' of github.com:benjaoming/django-wiki (3 years, 9 months ago) <benjaoming>
    |\  
    | * b096e34 - Update README.md (3 years, 9 months ago) <benjaoming>
    | * 60bc647 - Adding sekizai dep. (3 years, 9 months ago) <benjaoming>
    * | 750f6b4 - Adding history page, first class-based view, saving pointer to previous revision, better more strict handling of URLS (must always end with a /, except the root which must be "") (3 years, 9 months ago) <benjaoming>
    |/  
    * 8294826 - A few deployment details (3 years, 9 months ago) <benjaoming>
    * 58cf1a3 - Adding edit page, preview function and MORE. South migrations will be added back soon. (3 years, 9 months ago) <benjaoming>
    * dba6f82 - Adding template tags, bootstrap front end, creation of first root article, template tags for rendering (3 years, 9 months ago) <benjaoming>
    * 458bbd2 - Initial plugin and editor structure and base classes for extending MarkItUp editor in admin Creating images and attachments as plugins (3 years, 9 months ago) <benjaoming>
    * 2940142 - More work on models. Add Attachment model, and let attachments pass through a revision system. (3 years, 9 months ago) <benjaoming>
    * 322b5a6 - Finalizing URLPath as an MPTT model and generic relations on Articles (3 years, 9 months ago) <benjaoming>
    * 83fe3d4 - More on models. Not done yet. (3 years, 9 months ago) <benjaoming>
    * 30fb1ec - Begging to implement models (3 years, 9 months ago) <benjaoming>
    * 330c772 - Django south administration and URL patterns with default namespace (3 years, 9 months ago) <benjaoming>
    * ef2b1ec - Documentation with sphinx (3 years, 9 months ago) <benjaoming>
    * 357d9fa - Adding install instructions and setup.py (3 years, 9 months ago) <benjaoming>
    * 692aeae - Prepopulated test project. (3 years, 9 months ago) <benjaoming>
    * a3fe227 - typos (3 years, 9 months ago) <benjaoming>
    * 0e24a0b - typos (3 years, 9 months ago) <benjaoming>
    * de6c30b - Project skeleton, README with explanation of project (3 years, 9 months ago) <benjaoming>
    * aac85a2 - Update master (3 years, 10 months ago) <benjaoming>
    * ad97277 - Initial commit (3 years, 10 months ago) <benjaoming>