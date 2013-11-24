Latest Changes
==============
Compiled on: Sun Nov 24 23:11:39 CET 2013

    * 38252b8 - (HEAD, origin/master, origin/HEAD, master) #213 django 1.6 trouble fixed (5 days ago) <benjaoming>
    *   5538b39 - Merge branch 'master' of github.com:benjaoming/django-wiki (5 days ago) <benjaoming>
    |\  
    | * 5cab46e - Change requirements to use Pillow instead of PIL (6 days ago) <benjaoming>
    | * 127ada5 - Ah whatever... just delete everything about PIL!! (6 days ago) <benjaoming>
    | * 525b1b5 - PIL / Pillow related docs (6 days ago) <benjaoming>
    * | 974db28 - Add PyCharm ignores (6 days ago) <benjaoming>
    |/  
    * 40c6a4e - make README compatible with the pandoc translation to ReST (7 days ago) <benjaoming>
    * ffd2216 - Readme and Changelog update (7 days ago) <benjaoming>
    * 2f59ecb - version bump to 0.0.21 (7 days ago) <benjaoming>
    * 6e47242 - Fix #191 - introduce DRY in plugins.notifications default_url (7 days ago) <benjaoming>
    * 363f50a - Fix #206 by upgrading markitup to newer version (7 days ago) <benjaoming>
    * 34ac301 - Fix #207 and upgrade to jquery 1.10.2 (7 days ago) <benjaoming>
    * 57a3c97 - Fix #211 by adding a bit more clarity on the context variable handling (7 days ago) <benjaoming>
    * e08b54d - Fix bug in decorator causing double reverse lookups (7 days ago) <benjaoming>
    * e4d904e - Remove tests from plugins that are just stub implementations and not django 1.6 compat (10 days ago) <benjaoming>
    * a71b0ff - README updated (10 days ago) <benjaoming>
    * a5395e8 - syntax highlighting for README (10 days ago) <benjaoming>
    * 233bcf4 - Writing a few words on usage (10 days ago) <benjaoming>
    * 1db4378 - Add a screenshot (10 days ago) <benjaoming>
    * ab87c5a - Adding Travis tests for Django 1.6 (10 days ago) <benjaoming>
    * f1bad2d - automatically generate docs and CHANGELOG.md (10 days ago) <benjaoming>
    * b757c6d - Trying out a markdown formatted auto-gererated for new releases CHANGELOG (10 days ago) <benjaoming>
    * 22936c3 - Automating version number for sphinx (11 days ago) <benjaoming>
    * f232fd6 - django 1.6 fix for #191 - ArticleRevision.get_latest_by should be single field, not tuple (11 days ago) <benjaoming>
    * cc31f07 - django 1.6 and #191 BooleanField now has NULL value (11 days ago) <benjaoming>
    *   d0ea990 - Merge pull request #208 from stratatech/master (4 weeks ago) <benjaoming>
    |\  
    | * d8e872f - Russian translations fixes (4 weeks ago) <sminozhenko>
    | * 13c3e06 - Remove unnecessary lamba function (4 weeks ago) <sminozhenko>
    | * 164b416 - Russion translations + some missing label added + problem with transaltions in django_notify.settings.py (4 weeks ago) <sminozhenko>
    |/  
    *   b4d3be8 - Merge pull request #202 from rgcarrasqueira/master (4 weeks ago) <benjaoming>
    |\  
    | * 8ede8b8 - Bugfix request method is not found Django 1.4.7 (5 weeks ago) <Rogério Carrasqueira>
    | * 02f4bbe - Changing mptt to 0.5.3 (5 weeks ago) <Rogério Carrasqueira>
    | * e146a5d - Become compatible with django-cms 2.4.2 due django-sekizai (5 weeks ago) <Rogério Carrasqueira>
    * |   08758a6 - Merge pull request #203 from TomLottermann/master (5 weeks ago) <benjaoming>
    |\ \  
    | |/  
    |/|   
    | * ef4cccf - Updated translation. Fixed some minor issues. (5 weeks ago) <Thomas Lottermann>
    |/  
    * af767e3 - Instruction text for direct pip installation from git (8 weeks ago) <benjaoming>
    *   6104404 - Merge pull request #199 from TomLottermann/master (8 weeks ago) <benjaoming>
    |\  
    | * 29a03a3 - indentation fixed (8 weeks ago) <Thomas Lottermann>
    | * d3b52cf - pagination broke with bootstrap 3. It now works again! (8 weeks ago) <Thomas Lottermann>
    |/  
    *   db32a3e - Merge pull request #198 from TomLottermann/master (8 weeks ago) <benjaoming>
    |\  
    | *   be3b35d - Merge remote-tracking branch 'upstream/master' (8 weeks ago) <Thomas Lottermann>
    | |\  
    | |/  
    |/|   
    * | d07ba79 - fix #193 - only add style to input type=text/password (8 weeks ago) <benjaoming>
    * | c8d9307 - Fix [TOC] compatibility with custom ids and add support for [[WikiLink]] #179 (8 weeks ago) <benjaoming>
    * | c73d331 - remove bogus highlight plugin (8 weeks ago) <benjaoming>
    * |   809a12f - Merge branch 'master' of github.com:benjaoming/django-wiki (8 weeks ago) <benjaoming>
    |\ \  
    | * \   d956400 - Merge pull request #190 from yedpodtrzitko/master (8 weeks ago) <benjaoming>
    | |\ \  
    | | * | 085d4aa - bump translations (3 months ago) <yed_>
    | | * | e4e655e - show info about missing root instead of redirect to login (fix #174) (3 months ago) <yed_>
    * | | | 92cddce - add codehilite to default markdown extensions and close #134 (8 weeks ago) <benjaoming>
    |/ / /  
    * | |   e5cbdf4 - Merge branch 'master' of github.com:benjaoming/django-wiki (8 weeks ago) <benjaoming>
    |\ \ \  
    * | | | aca44f0 - fix #197 - use twitter typeahead (8 weeks ago) <benjaoming>
    * | | | 9716942 - ignore haystack test indexes (8 weeks ago) <benjaoming>
    | | | * b7c24ed - Group and owner can be null. The index must support this! (8 weeks ago) <Thomas Lottermann>
    | | |/  
    | |/|   
    | * |   51019fc - Merge pull request #192 from jbazik/master (3 months ago) <benjaoming>
    | |\ \  
    | | * | f1560a3 - Use a private instance of sorl.thumbnails. (3 months ago) <John Bazik>
    | |/ /  
    | * |   2314aa0 - Merge pull request #189 from yedpodtrzitko/master (3 months ago) <benjaoming>
    | |\ \  
    | | |/  
    | | *   05a5f53 - Merge remote-tracking branch 'orig/master' (3 months ago) <yed_>
    | | |\  
    | | |/  
    | |/|   
    | * |   0cb2ca2 - Merge pull request #188 from yedpodtrzitko/master (3 months ago) <benjaoming>
    | |\ \  
    |/ / /  
    | | * 30c45e2 - _change revision_ as a class-based view (3 months ago) <yed_>
    | |/  
    | * 10a4457 - create root as a class-based view (3 months ago) <yed_>
    |/  
    *   9528bf7 - Merge branch 'master' of github.com:benjaoming/django-wiki (3 months ago) <benjaoming>
    |\  
    | * 04ce91f - Update local.py (4 months ago) <benjaoming>
    * | 2c35ea7 - urlize also on last-of-line urls + fix icon (3 months ago) <benjaoming>
    |/  
    * 8fd557c - Fix #186 -- add empty local.py file (4 months ago) <benjaoming>
    *   8af2a61 - Merge branch 'master' of github.com:benjaoming/django-wiki (4 months ago) <benjaoming>
    |\  
    | * 8ffd8f0 - Fix #178 - improve urlize regex to accept everything after a domain, except spaces, [, and ( (4 months ago) <benjaoming>
    * | 05ecdbb - Fix #178 - improve urlize regex to accept everything after a domain, except spaces, [, and ( (4 months ago) <benjaoming>
    |/  
    * 2108a32 - grid layout on all form-action occurences (4 months ago) <benjaoming>
    * 5a90cfe - more issues in bootstrap 3 form widgets (4 months ago) <benjaoming>
    * bb89355 - textarea height and edit page button layout (4 months ago) <benjaoming>
    * 4aef17a - Fix #181 and #183 -- responsive modals, prepend for form inputs, form controls fixed for horizontal and vertical layouts (4 months ago) <benjaoming>
    * eb21b9d - bootstrap 3 compat on attachments plugin (4 months ago) <benjaoming>
    * 826b082 - fix 404 on respond.js (4 months ago) <benjaoming>
    *   3253098 - Merge branch 'master' of github.com:benjaoming/django-wiki (4 months ago) <benjaoming>
    |\  
    | *   5b34a24 - Merge pull request #185 from vezjakv/master (4 months ago) <benjaoming>
    | |\  
    | | * cbb815a - Init std.out stream handler compatable with Python 2.6 (4 months ago) <vezjakv>
    | |/  
    | * 27cc33c - Update README.md (4 months ago) <benjaoming>
    | * d059edb - SHA digest should display as link (4 months ago) <benjaoming>
    | * 515a1b7 - News update (4 months ago) <benjaoming>
    | * a594811 - Github Markdown broken on multiple comments in one line (4 months ago) <benjaoming>
    * | 8e77f06 - add codehilite note in README and a testproject settings module (4 months ago) <benjaoming>
    * | 06aa0e2 - add codehilite CSS to enable syntax highlighting for the codehilite Markdown extension (4 months ago) <benjaoming>
    * | e4382c8 - strip tags from Haystack searches (4 months ago) <benjaoming>
    * | 0cf10f5 - fix some more btn-default (4 months ago) <benjaoming>
    * | 47dee16 - fix btn-default in some other cases (4 months ago) <benjaoming>
    * | 9ccb216 - fix bootstrap btn-default class (4 months ago) <benjaoming>
    |/  
    * d8149a6 - fix #182 - bootstrap problem, not html (4 months ago) <benjaoming>
    * be42a26 - include font files in MANIFEST (4 months ago) <benjaoming>
    * d077af2 - responsive search form (4 months ago) <benjaoming>
    * fbccb07 - Fix search form on chromium (4 months ago) <benjaoming>
    * 657b8f9 - remove old bootstrap files (4 months ago) <benjaoming>
    * 34b9117 - refactor bootstrap grid layout (4 months ago) <benjaoming>
    * b919d54 - Upgrade to Bootstrap 3 RC1, add font-awesome, lots of refactoring (4 months ago) <benjaoming>
    * 204cc43 - make __init__.py always try to import settings.local (4 months ago) <benjaoming>
    * 91064d6 - Add SECRET_KEY to standard settings so testproject runs out of the box (4 months ago) <benjaoming>
    * e624b61 - Remove old settings_local.py (4 months ago) <benjaoming>
    * 04f131c - Add #django-wiki IRC channel - yay :) (4 months ago) <benjaoming>
    * 0f3bf03 - add setting WIKI_ACCOUNT_SIGNUP_ALLOWED (4 months ago) <benjaoming>
    * ebe1503 - Don't be verbose while scanning for plugins (4 months ago) <benjaoming>
    * 384fb62 - Fix #23 - move model registration from taking place within wiki.models to wiki.urls -- after all apps and models have been loaded (4 months ago) <benjaoming>
    * fcce3ce - cleanup (4 months ago) <benjaoming>
    * 5ff6fac - Fix #160 by allowing django-sendfile to be plugged in through settings.USE_SENDFILE (4 months ago) <benjaoming>
    * 0418642 - Fix #162 -- add filter_exclude to notify() (4 months ago) <benjaoming>
    * 02cb4d2 - Fix #164 by always setting a timeout for notification updates (4 months ago) <benjaoming>
    *   0bc8e32 - Merge branch 'master' of github.com:benjaoming/django-wiki (4 months ago) <benjaoming>
    |\  
    | * 0c148d3 - make possible for moderators to replace attachments (4 months ago) <benjaoming>
    * | 7846c81 - make possible for moderators to replace attachments, also fix #170, and remove catching all exceptions (4 months ago) <benjaoming>
    |/  
    * 8f65dd2 - Travis settings for test project (4 months ago) <benjaoming>
    *   3f3c903 - Fix #173 by letting articles refer to other article's attachments while checking the permissions of the original article owner (4 months ago) <benjaoming>
    |\  
    | * b9981cf - Updating travis test to use new settings layout (4 months ago) <benjaoming>
    * | 0090335 - Trying a new travis configuration since the PYTHON_PATH does not understand testproject.settings (4 months ago) <benjaoming>
    |/  
    * 112bba7 - cleanup (4 months ago) <benjaoming>
    * 88030a1 - Add Haystack search plugin (NB! Whoosh backend is broken upstream) (4 months ago) <benjaoming>
    * e21da47 - script to migrate south migrations to a custom auth user model (has already been run on wiki.migrations) (4 months ago) <benjaoming>
    * 58a46b8 - Refactore testproject.settings to accommodate more scenarios (4 months ago) <benjaoming>
    * a4e3ebf - make SEARCH_VIEW configurable from conf.settings (4 months ago) <benjaoming>
    * 24271db - cleanup unnecessary file (4 months ago) <benjaoming>
    * 810bd00 - Automatically generate README.rst for PyPi (4 months ago) <benjaoming>
    *   0c49222 - Merge branches 'master' and 'haystack' of github.com:benjaoming/django-wiki into haystack (4 months ago) <benjaoming>
    |\  
    | *   b9d969d - Merge pull request #172 from holdenweb/patch-1 (5 months ago) <benjaoming>
    | |\  
    | | * bcb47c9 - Update README.md (5 months ago) <Steve Holden>
    | |/  
    | *   3a06ff1 - Merge pull request #168 from TomLottermann/master (5 months ago) <benjaoming>
    | |\  
    | | *   a448f74 - Merge remote-tracking branch 'upstream/master' (5 months ago) <Thomas Lottermann>
    | | |\  
    | | |/  
    | |/|   
    | * | 39ecbdf - Cleanup 'admin' slug error message (5 months ago) <benjaoming>
    | * |   d9b2a5b - Merge pull request #166 from BenMarchant/patch-2 (5 months ago) <benjaoming>
    | |\ \  
    | | * | 0449a29 - Visitor cannot use admin as a slug (just in case !) (5 months ago) <BenMarchant>
    | |/ /  
    | * |   3d573b0 - Merge pull request #165 from BenMarchant/patch-1 (5 months ago) <benjaoming>
    | |\ \  
    | | * | be728b0 - Fixed: "wiki_footer_prepend block" (5 months ago) <BenMarchant>
    | |/ /  
    | | * 7b40385 - fixed non-found absolute wiki urls (5 months ago) <Thomas Lottermann>
    * | | 2c1e7c1 - Fix Django 1.4 incompatibility (4 months ago) <benjaoming>
    * | |   9c31dc3 - Merge branch 'haystack-search' of git://github.com/jdcaballero/django-wiki into jdcaballero-haystack-search (6 months ago) <benjaoming>
    |\ \ \  
    | |/ /  
    |/| |   
    | * |   784f8d6 - Merge pull request #1 from TomLottermann/haystack-search (6 months ago) <jdcaballero>
    | |\ \  
    | | * | 6108d30 - Minor fix (6 months ago) <Thomas Lottermann>
    | | * | e10d573 - Haystack 2.0 broke some stuff (site did not exist). This is fixed now. Furthermore we can use the highlighter by haystack. It does some stuff nicer than django-wikis (6 months ago) <Thomas Lottermann>
    | | * | e68272c - Some minor cleanup and same redirect behaviour on anonymous access (6 months ago) <Thomas Lottermann>
    | | * |   a1a25c2 - Merge remote-tracking branch 'jdcaballero/haystack-search' into haystack-search (6 months ago) <Thomas Lottermann>
    | | |\ \  
    | | |/ /  
    | |/| /   
    | | |/    
    | * | 4035783 - Permissions bare implementation (8 months ago) <Juan Diego Caballero>
    | * | ba667f1 - Paginator used to show the number of results (9 months ago) <Juan Diego Caballero>
    | * | 54c14bb - Initial Implementation of Search using Haystack (9 months ago) <Juan Diego Caballero>
    * | | dfe7be5 - hand empty notifications settings (6 months ago) <benjaoming>
    * | | d7df0af - pep8 cleanup (6 months ago) <benjaoming>
    * | | ed9d853 - Add notification interval to Article Settings page + New Notifications Settings page (6 months ago) <benjaoming>
    * | | 1d4faa9 - get_absolute_path added to Article model (6 months ago) <benjaoming>
    * | | 0a946c5 - Bootstrap 2.3.2 added and compatibility changes for dropdown menu (6 months ago) <benjaoming>
    * | | c24c882 - cleanup bootstrap (6 months ago) <benjaoming>
    | |/  
    |/|   
    * | c259b31 - Alter plugin API: BasePlugin.urlpatterns is now a dictionary (6 months ago) <benjaoming>
    * | ca59f20 - undo, only bad inheritance results in need of self.request set here (6 months ago) <benjaoming>
    * | 8bab47d - self.request on ArticleMixin view to allow for parent dispatch methods assuming its existence (6 months ago) <benjaoming>
    * | 0b9c2c5 - shorten database settings (6 months ago) <benjaoming>
    * | ac04cb6 - fix missing refactoring on renamed template block wiki_pagetitle (6 months ago) <benjaoming>
    * |   dfb9456 - Merge branch 'master' of github.com:benjaoming/django-wiki (6 months ago) <benjaoming>
    |\ \  
    | * | 00e4713 - Update README.md (6 months ago) <benjaoming>
    * | | 0d13578 - Fix #161 (mark accumulated notifications is_emailed=False) + clean up code + make notification email nicer (6 months ago) <benjaoming>
    |/ /  
    * |   a84eb16 - Merge branch 'master' of github.com:benjaoming/django-wiki (6 months ago) <benjaoming>
    |\ \  
    | * | b78edee - Update README.md (6 months ago) <benjaoming>
    * | | 00cf45b - (tag: alpha/0.0.20) Bump to 0.0.20 (6 months ago) <benjaoming>
    |/ /  
    * |   cc537a5 - Merge pull request #159 from TomLottermann/master (6 months ago) <benjaoming>
    |\ \  
    | * | 1bc5e48 - The management command now loads the language see https://docs.djangoproject.com/en/dev/howto/custom-management-commands/ for more details (6 months ago) <Thomas Lottermann>
    | * | 5c53280 - adding missing manifest information. language files were not included in the build. (6 months ago) <Thomas Lottermann>
    |/ /  
    * |   10c6444 - Merge pull request #157 from crazyzubr/master (6 months ago) <benjaoming>
    |\ \  
    | * | 6575a4a - simplify notify_settings (6 months ago) <crazyzubr>
    | * | dca3618 - fix notify_settings confuse (6 months ago) <crazyzubr>
    | * | f00af80 - filehandler django_notify in daemon mode (6 months ago) <crazyzubr>
    * | |   eabe615 - Merge pull request #156 from crazyzubr/master (6 months ago) <benjaoming>
    |\ \ \  
    | |/ /  
    | * | 3f08aec - fix (6 months ago) <crazyzubr>
    | * | 1006454 - add russian translation from django-notify (6 months ago) <crazyzubr>
    * | |   4fe5e47 - Merge pull request #155 from crazyzubr/master (6 months ago) <benjaoming>
    |\ \ \  
    | |/ /  
    | * | 90dde5a - fix errata (locale ru) (6 months ago) <crazyzubr>
    | * | 2d4eae2 - update locale ru (.po and .mo) (6 months ago) <crazyzubr>
    | * | fe8c7bd - Create django.po (6 months ago) <crazyzubr>
    |/ /  
    * |   69d209d - Merge pull request #153 from TomLottermann/master (6 months ago) <benjaoming>
    |\ \  
    | * | fd0ef6a - Updated german translations (6 months ago) <TomLottermann>
    |/ /  
    * |   1b7c241 - Merge branch 'master' of github.com:benjaoming/django-wiki (6 months ago) <benjaoming>
    |\ \  
    | * | 8b93d34 - Update TEMPLATE_CONTEXT_PROCESSORS instructions (6 months ago) <benjaoming>
    * | | 71880a2 - #145 do not break when AUTH_USER_MODEL is set on django<1.5 project (6 months ago) <benjaoming>
    * | | ad7b664 - Respect custom models (NB! current django 1.5.1 breaks wiki.views.accounts) #145 (6 months ago) <benjaoming>
    * | | 68e3478 - Remove spaces (6 months ago) <benjaoming>
    * | | 4e32ab6 - Add test suite that supports settings.AUTH_USER_MODEL and testing of South migrations #145 (6 months ago) <benjaoming>
    * | | 670c4d2 - #145 - add compatibility layer for importing users (6 months ago) <benjaoming>
    |/ /  
    * | 60c24e6 - Remove revisions to shrink prepopulated test db (6 months ago) <benjaoming>
    * | 03f0cc5 - vacuum sqlite test database and add new migrations (6 months ago) <benjaoming>
    * | e2d188b - Remember to call parent UserCreationForm.clean - fix username not tested for uniqueness in account handling (6 months ago) <benjaoming>
    * | 5d4c545 - BaseRevisionMixin.previous_revision: Allow deletion of Revisions by setting back-referenced revisions to NULL such that future revisions are not cascade deleted. (6 months ago) <benjaoming>
    * | e506c09 - Issue #145 - Add support for settings.AUTH_USER_MODEL both in model ForeignKey fields and South migrations. Backwards-compatible. (6 months ago) <benjaoming>
    * | 84c07e8 - #151 - missing translation calls (6 months ago) <benjaoming>
    * |   ec82837 - Merge branch 'master' of github.com:benjaoming/django-wiki (6 months ago) <benjaoming>
    |\ \  
    | * \   7a2103d - Merge pull request #150 from xiaclo/patch-1 (7 months ago) <benjaoming>
    | |\ \  
    | | * | ee85908 - Remove space from urlify.js path (7 months ago) <xiaclo>
    | |/ /  
    | * |   7e0f0a3 - Merge pull request #149 from TomLottermann/master (7 months ago) <benjaoming>
    | |\ \  
    | | * | 8782c84 - Slug stays fixed if the article already has a initial slug (7 months ago) <TomLottermann>
    | * | |   b5acff0 - Merge pull request #147 from TomLottermann/master (7 months ago) <benjaoming>
    | |\ \ \  
    | | |/ /  
    | | * |   6a69d88 - Merge remote-tracking branch 'upstream/master' (7 months ago) <TomLottermann>
    | | |\ \  
    | | |/ /  
    | |/| |   
    | * | | 7f172fb - Update README.md (7 months ago) <benjaoming>
    | | * | 493305b - Added wrapSelection to editor.js (7 months ago) <TomLottermann>
    * | | | 5b6c496 - (tag: alpha/0.0.19) Version bump (7 months ago) <benjaoming>
    |/ / /  
    * | | 61b3c61 - Make the urlize parser more strict (7 months ago) <benjaoming>
    * | | 36f3640 - add back anon read access to test main article (7 months ago) <benjaoming>
    * | | 31e2e60 - font size in blockquotes (7 months ago) <benjaoming>
    * | | 83c72bf - lock main article in the test project (7 months ago) <benjaoming>
    * | | dec9335 - Add attr_list to allow e.g. custom Header ids for custom references to header sections (7 months ago) <benjaoming>
    * | | 1a896ed - Markdown needs to be >2.2.0 due to 2.1.1 headerid extension tested broken with newer ElemenTree versions (7 months ago) <benjaoming>
    * | | 09e8af9 - less blahblah on the contribution stuff (8 months ago) <benjaoming>
    * | | 78bf232 - remove pip --use-mirrors (8 months ago) <benjaoming>
    * | |   6a1217c - Merge branch 'master' of github.com:benjaoming/django-wiki (8 months ago) <benjaoming>
    |\ \ \  
    | * \ \   60bcbbd - Merge pull request #143 from TomLottermann/master (8 months ago) <benjaoming>
    | |\ \ \  
    | | |/ /  
    | | * |   9ca5afb - Merge branch 'master' of github.com:TomLottermann/django-wiki (8 months ago) <TomLottermann>
    | | |\ \  
    | | | * | d4ce6ca - Fixed wrong icon when deleting article (8 months ago) <TomLottermann>
    | | * | | 06dc3ed - Fixed wrong icon when deleting article (8 months ago) <TomLottermann>
    | | |/ /  
    | * | |   d280dd4 - Merge pull request #142 from TomLottermann/master (8 months ago) <benjaoming>
    | |\ \ \  
    | | |/ /  
    | | * | a705f64 - version fix (8 months ago) <TomLottermann>
    | | * | 4cbc633 - version fix (8 months ago) <TomLottermann>
    | | * | 7188641 - Added translations for django_notify (8 months ago) <TomLottermann>
    | | * | acba7f7 - Respected changes, reformatted the lines (8 months ago) <TomLottermann>
    | |/ /  
    * | | c2f450b - fix SimplePlugin constructor - pull #144 (8 months ago) <benjaoming>
    |/ /  
    * |   ca5e28a - pull #141 - remove old test mechanism, try adding Warning failure (8 months ago) <benjaoming>
    |\ \  
    | * | 16f8e0b - pull #141 - add manage.py test + Django 1.5 to Travis config (8 months ago) <benjaoming>
    * | | e36f597 - pull #141 - remove old test mechanism, try adding Warning failure (8 months ago) <benjaoming>
    |/ /  
    * |   177bf3c - Merge pull request #141 from hynekcer/master (8 months ago) <benjaoming>
    |\ \  
    | * | eecd8a5 - Fixed on_article_delete_clear_cache. Some articles in the cache were not cleared and tests failed. (8 months ago) <Hynek Cernoch>
    | * | 2ad0694 - Added tests for clearing cache and for updating article_list (8 months ago) <Hynek Cernoch>
    | * | effc58a - Fixed on_article_delete if the article has children. (8 months ago) <Hynek Cernoch>
    | * | 44e4d7a - Added more tests and refactored the the first one. (8 months ago) <Hynek Cernoch>
    | * | 6dc14a1 - Fixed RuntimeWarning by replacing naive datetime by utc (8 months ago) <Hynek Cernoch>
    * | | d746543 - #140 - Markdown 2.2/2.3 API change - do not rely on markdown.extensions.headerid.unique (8 months ago) <benjaoming>
    |/ /  
    * | f6eb8be - French translation - changed msg id (att. pull #138) (8 months ago) <benjaoming>
    * | 8332ab6 - pull #139 - form data from args or kwargs (8 months ago) <benjaoming>
    * |   1aa8eb2 - Merge branch 'master' of github.com:benjaoming/django-wiki (8 months ago) <benjaoming>
    |\ \  
    | * | 4f0ef1a - pull #139 - form data from args or kwargs (8 months ago) <benjaoming>
    * | | 09f91ea - pull #139 - form data from args or kwargs (8 months ago) <benjaoming>
    |/ /  
    * |   159025b - Merge pull request #139 from hynekcer/master (8 months ago) <benjaoming>
    |\ \  
    | * | 634c3c0 - Revert "Fixed posting data to views.article.Preview" (8 months ago) <Hynek Cernoch>
    | * | 1bba4ec - Added recursion test for the current bug in preview. (8 months ago) <Hynek Cernoch>
    |/ /  
    * |   c3bbc37 - Do not use kwargs for permission methods (8 months ago) <benjaoming>
    |\ \  
    | * | 2d7957a - Do not use kwargs for permission methods (8 months ago) <benjaoming>
    * | | 37d9939 - Do not use kwargs for permission methods (8 months ago) <benjaoming>
    |/ /  
    * | d37e09c - #137 place permission logic ONLY in core.permissions and make article.can_read and article.can_write configurable (8 months ago) <benjaoming>
    * |   fdd36cd - Merge branch 'master' of github.com:benjaoming/django-wiki (8 months ago) <benjaoming>
    |\ \  
    | * \   de55506 - Merge pull request #138 from jdcaballero/master (8 months ago) <benjaoming>
    | |\ \  
    | | * \   054b3af - Merge remote-tracking branch 'origin/master' (8 months ago) <Juan Diego Caballero>
    | | |\ \  
    | | |/ /  
    | |/| |   
    | * | | 84dc39f - More clear PIL instructions. (8 months ago) <benjaoming>
    | | * | 5468b9a - Spanish translations added. (8 months ago) <Juan Diego Caballero>
    | | * | b74303e - Do not use HttpResponseRedirectBase anyways, just check status_code (8 months ago) <benjaoming>
    | | * | 43dbdd9 - fix imporerror for HttpResponseRedirectBase (8 months ago) <benjaoming>
    | | * | bc0eff8 - JSON view can return HttpResponseRedirect (8 months ago) <benjaoming>
    | | * | 71a6457 - changing apt-get to use python-imaging (8 months ago) <Dennis Coldwell>
    | | * | f76bc85 - adding PIL pre-req documentation (8 months ago) <Dennis Coldwell>
    * | | | 71c59d6 - fix wrong form target on clicking 'Switch to selected version' + modal window height (8 months ago) <benjaoming>
    |/ / /  
    * | | beb7571 - Do not use HttpResponseRedirectBase anyways, just check status_code (8 months ago) <benjaoming>
    * | | 6da0fd9 - fix imporerror for HttpResponseRedirectBase (8 months ago) <benjaoming>
    * | | 3f1ac96 - JSON view can return HttpResponseRedirect (8 months ago) <benjaoming>
    * | |   6a9539d - Merge branch 'master' of github.com:benjaoming/django-wiki (8 months ago) <benjaoming>
    |\ \ \  
    | |/ /  
    |/| |   
    | * |   f4f3a1d - Merge pull request #135 from coldwd/patch-1 (8 months ago) <benjaoming>
    | |\ \  
    | | * | ef83744 - changing apt-get to use python-imaging (8 months ago) <Dennis Coldwell>
    | | * | 4cf921f - adding PIL pre-req documentation (8 months ago) <Dennis Coldwell>
    | |/ /  
    * | | 0ff3fd4 - Fix #136 (8 months ago) <benjaoming>
    |/ /  
    * | e9bd946 - add clearfix for article tocs and indexes (8 months ago) <benjaoming>
    * | 5fdb93d - fix #130 - display disabled dropdown when no assignment permission (8 months ago) <benjaoming>
    * | 45cd25e - clean up block tags to be prefixed 'wiki_*' (8 months ago) <benjaoming>
    * |   0911c58 - Merge branch 'master' of github.com:benjaoming/django-wiki (8 months ago) <benjaoming>
    |\ \  
    | * \   914ecf5 - Merge pull request #132 from hynekcer/master (8 months ago) <benjaoming>
    | |\ \  
    | | * | 8f60a11 - Fixed typo in admin - Article revision list columns (8 months ago) <Hynek Cernoch>
    | |/ /  
    | * | a908af4 - Update README.md (8 months ago) <benjaoming>
    * | | 0344928 - Update to Bootstrap 2.3.1 and simplify LESS import statements (8 months ago) <benjaoming>
    |/ /  
    * | 428d236 - (tag: alpha/0.0.18) Bump to 0.0.18 (8 months ago) <benjaoming>
    * | 85602fe - Fix #125 - missing redirect call (8 months ago) <benjaoming>
    * |   807611b - Merge pull request #131 from daltonmatos/translation/pt_BR (8 months ago) <benjaoming>
    |\ \  
    | * | 5779039 - Adding translation for pt_BR (8 months ago) <Dalton Barreto>
    |/ /  
    * |   2cd0dbe - Merge pull request #129 from TomLottermann/master (8 months ago) <benjaoming>
    |\ \  
    | * | dc6a2aa - reset readme and removed mo ignorance from gitignore, since it is needed (8 months ago) <TomLottermann>
    | * | 548cc81 - complete set of languages (8 months ago) <TomLottermann>
    | * | 62b37b3 - compiled recent version (8 months ago) <TomLottermann>
    | * | 757f24a - Plugins are a WIP (8 months ago) <TomLottermann>
    | * | b694a89 - right names (8 months ago) <TomLottermann>
    | * | 3339ae4 - fixes to the manifest (8 months ago) <TomLottermann>
    | * | 69a4b2d - german locale (8 months ago) <TomLottermann>
    | * | 9da762d - Compilation of german locale (8 months ago) <TomLottermann>
    | * | d9b997b - initial translation done (without the plugins) (8 months ago) <TomLottermann>
    | * | a6182dd - start of translations (8 months ago) <TomLottermann>
    | * | 59b6558 - start of translations (8 months ago) <TomLottermann>
    | * | 8efc4bd - readme changed (8 months ago) <TomLottermann>
    |/ /  
    * |   75a0581 - Merge branch 'master' of github.com:benjaoming/django-wiki (9 months ago) <benjaoming>
    |\ \  
    | * | 2b28521 - Update README.md (9 months ago) <benjaoming>
    | * |   17b15d9 - Merge pull request #124 from SacNaturalFoods/master (9 months ago) <benjaoming>
    | |\ \  
    | | * | 3add05a - fixed _clear_ancestor_cache call (9 months ago) <tschmidt>
    | * | |   bc57765 - Merge pull request #122 from SacNaturalFoods/master (9 months ago) <benjaoming>
    | |\ \ \  
    | | |/ /  
    | | * | 088e2de - moved article save and delete clear cache signal handlers to Article model (9 months ago) <tschmidt-dev>
    | | * | 217fea9 - refactored urlpath._clear_ancenstor_cache to use article.ancenstor_objects generator (9 months ago) <tschmidt-dev>
    | | * |   7a2985c - merge (9 months ago) <tschmidt-dev>
    | | |\ \  
    | | * | | e20b2d6 - clear ancestor cache on save and delete article so that things like article_lists are refreshed (9 months ago) <tschmidt>
    | | | |/  
    | | |/|   
    * | | | 6641ed1 - use self.stdout in django_notify management script logging (see django docs: https://docs.djangoproject.com/en/dev/howto/custom-management-commands/) (9 months ago) <benjaoming>
    |/ / /  
    * | | df27e51 - Fixed posting data to views.article.Preview (9 months ago) <benjaoming>
    | |/  
    |/|   
    * | c775a18 - #111 Add ancestor generator to Article (9 months ago) <benjaoming>
    |/  
    * 9ca892d - Do not use URLField, it does not allow relative paths (9 months ago) <benjaoming>
    * 7ec137f - Redirect from sign up and login pages for logged in users. Use wiki:root url for root article. (9 months ago) <benjaoming>
    * 0af4af2 - #119 restore if image deleted and uploading new image file (9 months ago) <benjaoming>
    * b73278c - remove initial blank attachments and images (9 months ago) <benjaoming>
    * 7f6acb7 - #119 do not fail when deleting blank image and attachment fields (9 months ago) <benjaoming>
    * 51497ca - page title for signup page (9 months ago) <benjaoming>
    *   c06108c - Merge branch 'master' of github.com:benjaoming/django-wiki (9 months ago) <benjaoming>
    |\  
    | *   c8eeab5 - Merge branch 'master' of github.com:benjaoming/django-wiki (9 months ago) <benjaoming>
    | |\  
    * | \   6e9f4f5 - Add a simple honeypot for signups #116 (9 months ago) <benjaoming>
    |\ \ \  
    | |/ /  
    |/| /   
    | |/    
    | * a570d0a - Add a simple honeypot for signups (9 months ago) <benjaoming>
    * | acd9636 - Add a simple honeypot for signups #117 (9 months ago) <benjaoming>
    |/  
    *   2173d4b - Merge pull request #117 from jdcaballero/master (9 months ago) <benjaoming>
    |\  
    | * c96d656 - User creation form extendedto include email as a required field (9 months ago) <Juan Diego Caballero>
    | *   3932d27 - Merge branch 'master' of https://github.com/benjaoming/django-wiki (9 months ago) <Juan Diego Caballero>
    | |\  
    | * | f0b25a5 - UserCreateForm subclassed to include the email as a required parameter in the signup. (9 months ago) <Juan Diego Caballero>
    * | | 80790d5 - #118 django 1.5 (9 months ago) <benjaoming>
    * | | 3950de5 - Fix #118 Avoid deprecation warning in Django 1.5 (9 months ago) <benjaoming>
    * | |   e091f01 - Merge branch 'master' of github.com:benjaoming/django-wiki (9 months ago) <benjaoming>
    |\ \ \  
    | * | | c6f9ee5 - Fix #118 Avoid deprecation warning in Django 1.5 (9 months ago) <benjaoming>
    * | | | 6367157 - Fix #118 (forgot django_notify) Avoid deprecation warning in Django 1.5 (9 months ago) <benjaoming>
    |/ / /  
    * | | 098faa1 - Add note in pluginbase about use of Meta.app_label (9 months ago) <benjaoming>
    * | | b20094c - Inherit from EmptyQuerySet (9 months ago) <benjaoming>
    | |/  
    |/|   
    * | a4f9d3b - Few more readme changes (9 months ago) <benjaoming>
    * | ead17b0 - Todo and readme updates (9 months ago) <benjaoming>
    * |   65c882b - Merge branch 'master' of github.com:benjaoming/django-wiki (9 months ago) <benjaoming>
    |\ \  
    | |/  
    | * efb617e - Update to 0.0.17 (9 months ago) <benjaoming>
    * | a7254ab - (tag: alpha/0.0.17) bump to 0.0.17 (9 months ago) <benjaoming>
    |/  
    * bfec4e8 - rename command, cleanup code, add logging (9 months ago) <benjaoming>
    * 15b02ae - ignore settings_local (9 months ago) <benjaoming>
    * 1e9d5b5 - remove print stm (9 months ago) <benjaoming>
    * bcddb0b - Support and contributions (9 months ago) <benjaoming>
    * d913907 - Support and contributions (9 months ago) <benjaoming>
    *   088c0fe - Merge pull request #115 from jdcaballero/master (9 months ago) <benjaoming>
    |\  
    | * fbd75ae - Subject changed to a translated string, notification email changed to @example.com (9 months ago) <Juan Diego Caballero>
    | * c13d97d -  Notifications Implementation: (9 months ago) <Juan Diego Caballero>
    | * a47c6da - Revert "Email Notifications Implementation" (9 months ago) <Juan Diego Caballero>
    | * 700bb6e - Email Notifications Implementation (9 months ago) <Juan Diego Caballero>
    |/  
    * e448e2b - Replace Markdown toc extension and add improved version to macro package. (9 months ago) <benjaoming>
    * 9655067 - bootstrap typography (9 months ago) <benjaoming>
    * ea70181 - bootstrap typography and remove extra <li>s on article_list (9 months ago) <benjaoming>
    * 61131d8 - (tag: alpha/0.0.16) bump to 0.0.16 (9 months ago) <benjaoming>
    * d66234e - cache key should be from current revision (9 months ago) <benjaoming>
    * 089dd2f - restore lost-and-found auto collection if subtrees are disconnected (9 months ago) <benjaoming>
    * fa3c916 - soft linebreak after images to conserve preceeding headline elements (9 months ago) <benjaoming>
    * db07ac2 - invalidate article cache when plugins are updated (9 months ago) <benjaoming>
    * 1dd4788 - thumbnail styles (9 months ago) <benjaoming>
    * db73b51 - redirect for delete view to parent (9 months ago) <benjaoming>
    * dcf7e72 - fix article purging (9 months ago) <benjaoming>
    * c57656a - only show active children in article_list (9 months ago) <benjaoming>
    * 701e34b - show article titles instead of slugs in index view (9 months ago) <benjaoming>
    * ea1b3ad - allow inline attachment tag (9 months ago) <benjaoming>
    * fc94f67 - do not show deleted files in list, add separate restore menu item (9 months ago) <benjaoming>
    * fc9efa6 - non-zip files fix for moderators and clean up a bit (9 months ago) <benjaoming>
    * e85cbc6 - title for TOCs (9 months ago) <benjaoming>
    * b0a6d6e - bootstrap styling (9 months ago) <benjaoming>
    * dfb5693 - python 2.5 compatibility for zip archives (9 months ago) <benjaoming>
    * 1b5b583 - zip file uploading and extracting for moderators (9 months ago) <benjaoming>
    * 4f019e7 - raise 404 if plugin is missing (9 months ago) <benjaoming>
    * 0cabdfb - refactor article view to use view.html template (9 months ago) <benjaoming>
    * 0579521 - fix spam protection wrongly targetting moderators (9 months ago) <benjaoming>
    * 44b1e2f - Make cache timeout configurable and remove erred block tags from render.html (9 months ago) <benjaoming>
    * 0d092fa - improve resizable to properly fit nested iframes etc (10 months ago) <benjaoming>
    * ecaccbd - add request context processor and check that config is OK (10 months ago) <benjaoming>
    * 6a3c777 - resizable modals (10 months ago) <benjaoming>
    * e4d0669 - add template assignment tag login_url (10 months ago) <benjaoming>
    * 73af524 - broken boostrap-responsive build (10 months ago) <benjaoming>
    * be19fdb - do not show deleted articles in article_list macro (10 months ago) <benjaoming>
    *   6be1a3d - Merge branch 'master' of github.com:benjaoming/django-wiki (10 months ago) <benjaoming>
    |\  
    | * eb3bd0b - Update README.md (10 months ago) <benjaoming>
    * | e6e0a84 - Add better info about licensing (10 months ago) <benjaoming>
    |/  
    * d25da1c - (tag: alpha/0.0.15) Bump to 0.0.15 (10 months ago) <benjaoming>
    * 51daba0 - add model chart in pdf to the build-sdist process (10 months ago) <benjaoming>
    * e7c70fd - typo (10 months ago) <benjaoming>
    * 89b64aa - modify build to clean up old egg dir and add back the MANIFEST.in symlink (10 months ago) <benjaoming>
    * d568683 - python 2.5 support (10 months ago) <benjaoming>
    * 2c39d15 - do not fail when removing images located in non-existing dirs (10 months ago) <benjaoming>
    * 628b59c - image plugin thumbnail css (10 months ago) <benjaoming>
    * 948580c - image plugin thumbnail css (10 months ago) <benjaoming>
    * da15d5d - use LESS for stylesheets by extending twitter-bootstrap (10 months ago) <benjaoming>
    * 76a3532 - rm dupe lines (10 months ago) <benjaoming>
    * f0c3458 - footer clearfix (10 months ago) <benjaoming>
    *   ece1239 - Merge branch 'master' of github.com:benjaoming/django-wiki (10 months ago) <benjaoming>
    |\  
    | *   94e6035 - Merge pull request #108 from SacNaturalFoods/master (10 months ago) <benjaoming>
    | |\  
    | | * 26c922b - removed overlooked debug print statements (10 months ago) <tschmidt-dev>
    | | * 4d34e70 - fixed macro arg regex for args longer than 1 character (10 months ago) <tschmidt-dev>
    | |/  
    * | abe7282 - unfinished generic markdown extension (10 months ago) <benjaoming>
    * | 53205ac - fix setting article fk on reusable plugins for identifying permissions (10 months ago) <benjaoming>
    |/  
    * 7e6da88 - (tag: alpha/0.0.14) Bump to 0.0.14 (10 months ago) <benjaoming>
    * 67d8cf3 - Security fix, do not call eval on input (10 months ago) <benjaoming>
    * d9d19f0 - fix python 2.5 unknown elementree method (10 months ago) <benjaoming>
    * f9a46f1 - (tag: alpha/0.0.13) Note on python 2.5 and improve article list (10 months ago) <benjaoming>
    * c4e855d - Update README.md (10 months ago) <benjaoming>
    * 076ad8e - Python 2.5 support note (10 months ago) <benjaoming>
    * 0106b6f - python 2.5 support (10 months ago) <benjaoming>
    * b86be8c - (tag: alpha/0.0.12) version bump to 0.0.12 (10 months ago) <benjaoming>
    * d5f8352 - Fix #100 add print CSS and remove inline <style> (10 months ago) <benjaoming>
    * 9070358 - Fix error in macros removing unknown tags from stack and prettify styling (10 months ago) <benjaoming>
    * ff9ad26 - add a few more default markdown plugins (10 months ago) <benjaoming>
    * 2ed231a - Apply user info on the creater of the first revision of the root article (10 months ago) <benjaoming>
    * c50e05f - Display a helping exception message when MPTT is failing (10 months ago) <benjaoming>
    * e25b3a4 - logo block for footer (10 months ago) <benjaoming>
    * 1b06fb0 - Fix example code (10 months ago) <benjaoming>
    * 2aabc2d - move macros configuration and do not include django_notify twice in the urlconf (10 months ago) <benjaoming>
    * affa159 - Make django notify admin configurable so it can be excluded (10 months ago) <benjaoming>
    *   d004700 - Merge branch 'master' of github.com:benjaoming/django-wiki (10 months ago) <benjaoming>
    |\  
    | *   365793d - Merge pull request #107 from SacNaturalFoods/master (10 months ago) <benjaoming>
    | |\  
    | | * 22486f5 - added kwargs logic to macros plugin and depth kwarg to article_list macro (10 months ago) <tschmidt-dev>
    | |/  
    * | b336586 - Add help sidebar for macros and make allowed methods configurable (10 months ago) <benjaoming>
    |/  
    * 0751cc8 - using wrong class for widget when in readonly mode on some settings form fields (10 months ago) <benjaoming>
    * 86ee414 - receive post_save signal only using kwargs (10 months ago) <benjaoming>
    * 91076f2 - security fix for macro plugin, add plugins.acros to testproject (10 months ago) <benjaoming>
    *   933ac19 - Merge pull request #105 from SacNaturalFoods/master (10 months ago) <benjaoming>
    |\  
    | * d6f3724 - restructured url resolver in article_list macro (10 months ago) <tschmidt-dev>
    | * c0d5f25 - fixed article_list macro sublist markup (10 months ago) <tschmidt-dev>
    | * a7bbf18 - added Django 1.5 url syntax to macros plugin; added condition to avoid generating empty lists for each child in article_list macro (10 months ago) <tschmidt-dev>
    | * 5eda878 - added wiki-article-sublist class to article_list macro template (10 months ago) <tschmidt-dev>
    | * 3493af1 - added wiki-article-list class to article_list macro template (10 months ago) <tschmidt-dev>
    | * 5a3c029 - added core macros plugin with initial article_list macro (10 months ago) <tschmidt-dev>
    * |   919d45e - Merge pull request #104 from SacNaturalFoods/master (10 months ago) <benjaoming>
    |\ \  
    | |/  
    | * f14ecef - collapsed MARKDOWN_EXTENSIONS and MARKDOWN_SAFE_MODE settings into MARKDOWN_KWARGS (10 months ago) <tschmidt-dev>
    * | f58974d - Update README.md (10 months ago) <benjaoming>
    * | 4bf8769 - Update README.md (10 months ago) <benjaoming>
    * |   61e5952 - Merge branch 'master' of github.com:benjaoming/django-wiki (10 months ago) <benjaoming>
    |\ \  
    | * | 603898f - Update README.md (10 months ago) <benjaoming>
    | * | 3167e4b - Update README.md (10 months ago) <benjaoming>
    | * | 281e276 - Update README.md (10 months ago) <benjaoming>
    * | | c93f3c5 - add debug_toolbar if installed (10 months ago) <benjaoming>
    |/ /  
    * |   27f5b44 - Merge branch 'master' of github.com:benjaoming/django-wiki (10 months ago) <benjaoming>
    |\ \  
    | * \   23f48b3 - Merge pull request #102 from SacNaturalFoods/master (10 months ago) <benjaoming>
    | |\ \  
    | | |/  
    | | * 0f02092 - added MARKDOWN_SAFE_MODE setting (10 months ago) <tschmidt-dev>
    | | * 8ac9814 - fixed help plugin TOC syntax and added Tables section (10 months ago) <tschmidt-dev>
    | * |   31562fd - Merge branch 'master' of github.com:benjaoming/django-wiki (10 months ago) <benjaoming>
    | |\ \  
    * | | | 68fc90c - Add settings for inheriting owner and group permissions and fix #99 (10 months ago) <benjaoming>
    * | | |   b1b3aea - Merge branch 'master' of github.com:benjaoming/django-wiki (10 months ago) <benjaoming>
    |\ \ \ \  
    | |/ / /  
    |/| / /   
    | |/ /    
    | * | c21775d - Use Form Media for SelectWidgetBootstrap and update wiki_form templatetag (10 months ago) <benjaoming>
    | |/  
    * | 9c5f46d - Use Form Media for SelectWidgetBootstrap and update wiki_form templatetag Fix #95 (10 months ago) <benjaoming>
    |/  
    * efd8db8 - WARNING! May break your config: Clean up settings variale names in images and attachments plugins and use unified defaults. Issue #91. (10 months ago) <benjaoming>
    *   6b9f346 - Merge pull request #92 from gluwa/master (10 months ago) <benjaoming>
    |\  
    | * 55a4a5b - in attachments plugin, append '.upload' to uploaded files only when settings.APPEND_EXTENSION is True. (10 months ago) <Tae-lim Oh>
    | * 15a33ea - adding custom storage backend option to images plugin (10 months ago) <Tae-lim Oh>
    |/  
    *   64a22a8 - Merge branch 'master' of github.com:benjaoming/django-wiki (11 months ago) <benjaoming>
    |\  
    | * 5f90b18 - Update README.md (11 months ago) <benjaoming>
    * | 453131e - add testproject template dir (11 months ago) <benjaoming>
    * | 59567e3 - Error pages for test project (11 months ago) <benjaoming>
    |/  
    * 9664ce1 - Add PIL to requirements.txt and remove Python 2.5 from travis (11 months ago) <benjaoming>
    * 3607ea8 - test with manage.py (11 months ago) <benjaoming>
    * 659d145 - fix double requirement (11 months ago) <benjaoming>
    *   6c7f905 - Merge branch 'master' of github.com:benjaoming/django-wiki (11 months ago) <benjaoming>
    |\  
    | * 62d2c4f - Update README.md (11 months ago) <benjaoming>
    * | 558d88c - fix pip argument for travis (11 months ago) <benjaoming>
    |/  
    * 3b2aceb - travis config added (11 months ago) <benjaoming>
    * 09cab11 - missing template load stm (11 months ago) <benjaoming>
    * c14ee73 - Use JS to save article form data on all sidebar plugin forms (11 months ago) <benjaoming>
    * 2e36575 - Scroll if there are many images, only warn about unsaved changes if there are in fact such (11 months ago) <benjaoming>
    * fb40d08 - Avoid losing user data when a sidebar form is called and article contents have been modified #33 (11 months ago) <benjaoming>
    * b9e95ef - Support for I10N - use timezone.now (11 months ago) <benjaoming>
    * ab45a20 - Cleanup nicely when an image or attachment is deleted - remove the file and any empty directories #25 (11 months ago) <benjaoming>
    * 36eb1f8 - Do not allow merging with a deleted revision #27 (11 months ago) <benjaoming>
    * 652433f - Remove unused setting (11 months ago) <benjaoming>
    * 8a010d8 - apply migrations to prepopulated test database (11 months ago) <benjaoming>
    * 6eb99d2 - Account handling system should pass all django.contrib.auth test cases #86 (11 months ago) <benjaoming>
    * ea2cd01 - Account handling system should pass all django.contrib.auth test cases #86 (11 months ago) <benjaoming>
    * df59145 - Redirect for the built-in account handling when login is required + better err page. (11 months ago) <benjaoming>
    * c805fee - Add link to forum/mailing list (11 months ago) <benjaoming>
    * ac826e3 - sorl.thumbnail in INSTALLED_APPS + copy-paste friendly (11 months ago) <benjaoming>
    * e8dcb97 - Update README.md (11 months ago) <benjaoming>
    * bde97a5 - Update README.md (11 months ago) <benjaoming>
    * 97734d0 - Update README.md (11 months ago) <benjaoming>
    * f482b0c - Bumping to version 0.0.9 for new PyPi release (11 months ago) <benjaoming>
    * 3add660 - Remove 'center' from javascript prompt help text (#88) (12 months ago) <benjaoming>
    * 2c0b35a - Add local settings to testproject (1 year ago) <benjaoming>
    * 82b4e32 - #71 and #87 - put the 'get' by path pattern at the very end of all patterns (1 year ago) <benjaoming>
    * 9604209 - #71 - missing pattern 'get' in new class based urls (1 year ago) <benjaoming>
    *   a106977 - Merge pull request #85 from shaunc/master (1 year ago) <benjaoming>
    |\  
    | * f0592f5 - fixes merge (1 year ago) <Shaun Cutts>
    | *   9a38e27 - merges recent changes w/ classurl branch (1 year ago) <Shaun Cutts>
    | |\  
    |/ /  
    | * f8900d0 - adds class for url configuration (1 year ago) <Shaun Cutts>
    | * 5e812ac - updates {% url %} use in notifications menubaritem template to confrom to django 1.5 (1 year ago) <Shaun Cutts>
    * | c93b318 - Be explicit about application order (#84) (1 year, 1 month ago) <benjaoming>
    * |   ceb705b - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 1 month ago) <benjaoming>
    |\ \  
    | * | 6704790 - Retry: Fix settings.py link (#81) (1 year, 1 month ago) <benjaoming>
    | * | f84a092 - Fix settings.py link (#81) (1 year, 1 month ago) <benjaoming>
    | * | d586040 - Fix settings.py link (1 year, 1 month ago) <benjaoming>
    * | | 32591c2 - Regression from adding spam protection, missing argument in when view class Preview initialized EditForm (#83) (1 year, 1 month ago) <benjaoming>
    |/ /  
    * | 2cb3950 - Move all javascript to load at the bottom of the page and ensure only to add javascript inside Sekizai addtoblock tag. (#54) (1 year, 1 month ago) <benjaoming>
    * | 109421e - Fix markdown extension for images to allow no align:xx specified and use bootstrap pull-left and pull-right. Don't allow center alignment. (#65) (1 year, 1 month ago) <benjaoming>
    * | 1834071 - Add spam/bot protection by verifying user session and ip_address and check the number of recent revisions (#72) Add global setting to disable anonymous article creation (#72) (1 year, 1 month ago) <benjaoming>
    * | ecbacc8 - Count number of occurences of the same message and display "x times" in the notification list instead of duplicate messages. (1 year, 1 month ago) <benjaoming>
    * | ea71c5c - Add warning on Edit page if user is not logged in w/ link to login page and redirect back to edit page (#55) (1 year, 1 month ago) <benjaoming>
    * | 58cb725 - eh..remove alert() (1 year, 1 month ago) <benjaoming>
    * | ce1ff2e - Setting Colorbox.js width and height (#69) and adding captions. (1 year, 1 month ago) <benjaoming>
    * |   2458217 - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 1 month ago) <benjaoming>
    |\ \  
    | * | cb3d251 - Ensure that CreateForm fails when slug field is longer than the maximum allowed slug length (#54). (1 year, 1 month ago) <benjaoming>
    * | | 1dbd51f - Ensure that CreateForm fails when slug field is longer than the maximum allowed slug length (#57) (1 year, 1 month ago) <benjaoming>
    |/ /  
    * | 393aa34 - Adding check on article locked for attachments. (#74) - Also cleaning up attachment list and removing forms when article is locked. Adding template filter is_locked (1 year, 1 month ago) <benjaoming>
    * | 9d801fb - Adding Bootstrap 2.2.0 (1 year, 1 month ago) <benjaoming>
    * |   e948b73 - Merge pull request #79 from avtobiff/update-readme-dependencies (1 year, 1 month ago) <benjaoming>
    |\ \  
    | * | f31b6d4 - Correct django dependency invariant (1 year, 1 month ago) <Per Andersson>
    | * | 78fa3a8 - Increase django-mptt dependency version (1 year, 1 month ago) <Per Andersson>
    |/ /  
    * |   f3f667e - Merge pull request #75 from jdcaballero/master (1 year, 1 month ago) <benjaoming>
    |\ \  
    | * | 0f422c0 - Update wiki/plugins/notifications/forms.py (1 year, 1 month ago) <jdcaballero>
    |/ /  
    * | e7d64e1 - Never return a proxy object from __unicode__ ! (#73) (1 year, 1 month ago) <benjaoming>
    * |   46fc152 - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 1 month ago) <benjaoming>
    |\ \  
    | |/  
    | *   2288efd - Merge pull request #64 from webdevelop/master (1 year, 1 month ago) <benjaoming>
    | |\  
    | | * d77930c - Greedy regex algorithm (1 year, 1 month ago) <Vladyslav>
    * | | a479748 - Never return a proxy object from __unicode__ ! (#73) (1 year, 1 month ago) <benjaoming>
    |/ /  
    * | 0c8a554 - Issue #68 - Add sorl-thumbnail to dependencies. Furthermore, add >=0.5.3 to django-mptt which has caused some reports. Read requirements.txt into setup.py to avoid hard coding and mismatches. Create 0.0.2 release which is not broken because README.md was missing from distribution file. (1 year, 1 month ago) <benjaoming>
    * | 5db399c - Issue #67 - left joins caused by m2m fields sometimes result in duplicate rows, applying distinct() (1 year, 1 month ago) <benjaoming>
    * | 0850915 - Fix Issue #66 (1 year, 1 month ago) <benjaoming>
    * | d08301f - Fix transaction support for uploading attachments (1 year, 2 months ago) <benjaoming>
    * | ee08a7f - Fix #60 - do not allow empty image form fields even though the model should handle it. (1 year, 2 months ago) <benjaoming>
    * | 520e123 - Fixing long titles in notifications and display total count of notifications instead of just a truncated number. (1 year, 2 months ago) <benjaoming>
    * | a886040 - Cosmetic changes to fix #38 - but otherwise there is no rules for URL lengths other than IE setting the lower limit at 2048 characters which should hardly annoy anyone. (1 year, 2 months ago) <benjaoming>
    * | 8884709 - Remove redundant table (1 year, 2 months ago) <benjaoming>
    * | bbd4234 - Issue#50 - make using send_file configurable to allow for remote storage backends such as S3. (1 year, 2 months ago) <benjaoming>
    * |   1082aef - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 2 months ago) <benjaoming>
    |\ \  
    | * | 0bc5611 - Update README.md (1 year, 2 months ago) <benjaoming>
    | * |   4e2ced2 - Merge pull request #62 from webdevelop/master (1 year, 2 months ago) <benjaoming>
    | |\ \  
    | | |/  
    | | * e0a3b99 - Uncode filename in US-ASCII format, needable for russian and other language (1 year, 2 months ago) <Vladyslav>
    | | * f723c60 - Change max_length of file to 255 for handling files with big name (1 year, 2 months ago) <Vladyslav>
    | * | 9e3a9d0 - Adding news section about RC1. (1 year, 2 months ago) <benjaoming>
    | |/  
    | *   4f750cd - Merge pull request #52 from pypetey/master (1 year, 2 months ago) <benjaoming>
    | |\  
    | | * 0fd815b - small fix for extra hash (1 year, 2 months ago) <pypetey>
    | | * 3183706 - Fix for line 561 error: 'msgid' format string with unnamed arguments cannot be properly localized: The translator cannot reorder the arguments. Please consider using a format string with named arguments, and a mapping instead of a tuple for the arguments. (1 year, 2 months ago) <pypetey>
    | |/  
    * | 2a9167a - Add support for counting duplicate notifications instead of repeating the same. (1 year, 2 months ago) <benjaoming>
    |/  
    * 0fa8bad - Use safe preprocessors for attachments and images plugin. Fix Issue #39. Also use a template to render attachments html. (1 year, 3 months ago) <benjaoming>
    * 8d1dd37 - Updating model chart to reflect current project status (1 year, 3 months ago) <benjaoming>
    * 9503fac - Issue #50 do not use full paths because remote storage does not implement this. (1 year, 3 months ago) <benjaoming>
    * 8f64202 - Issue #48: Searches should be case insensitive (1 year, 3 months ago) <benjaoming>
    * b68f0b5 - More modifications for pypi, first 0.0.1 released - pip install wiki (1 year, 3 months ago) <benjaoming>
    * 996800c - Adding a MANIFEST for pypi distribution (1 year, 3 months ago) <benjaoming>
    * da4e421 - Fixing issues with PYPI compatibility (1 year, 3 months ago) <benjaoming>
    *   8a589bb - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <benjaoming>
    |\  
    | *   c7aa2e1 - Merge pull request #40 from uAnywhere/master (1 year, 3 months ago) <benjaoming>
    | |\  
    | | * 4e6cdda - Minor optimisation to ACLs (use .exists() instead of bool() because it's faster), fix an issue on Django 1.5 where EmptyQuerySet has no method select_related_common() (1 year, 3 months ago) <Michael Farrell>
    | |/  
    * | 3a31f2c - Do not conditionally include login, logout and signup URLs in urlpatterns. Handle WIKI_ACCOUNT_HANDLING inside views. Issue #43. (1 year, 3 months ago) <benjaoming>
    |/  
    *   76b0698 - Merge branch 'edx_release' (1 year, 3 months ago) <benjaoming>
    |\  
    | * 7fad1ac - (origin/edx_release) Removing settings from links plugin (1 year, 3 months ago) <benjaoming>
    | * d489d13 - Merging with edx branch, fixing link plugin to not use live_lookups (it's meaningless because whole articles are normally cached and therefore, links are not resolved at every article view). Also, settings for the links plugin were wrongly placed in the main settings file. (1 year, 3 months ago) <benjaoming>
    | *   72faa3b - Merge pull request #31 from rocha/edx_release (1 year, 3 months ago) <benjaoming>
    | |\  
    | | * cd1c23e - Fixed WikiPath regexp. It was incorrectly matching [Title](Link) on the same line. (1 year, 3 months ago) <Carlos Andrés Rocha>
    | |/  
    | * 7e42bce - Changed behavior of wikilinks extension to optionally disable database and prefer to stay at a certain level. (1 year, 3 months ago) <Bridger Maxwell>
    | * f00b7d3 - Fixed bug where non-found wiki links ignored base url. (1 year, 3 months ago) <Bridger Maxwell>
    | * 533c7fc - Dir links are now prominently view links with arrows for viewing children. (1 year, 3 months ago) <Bridger Maxwell>
    | * d1b97e2 - Fixed bug for calling .active() on empty query sets. (1 year, 3 months ago) <Bridger Maxwell>
    | * 50c08a3 - Added setting for disabling SelectWidgetBootstrap. (1 year, 3 months ago) <Bridger Maxwell>
    | * 3576a2d - Allowing periods in slug for wikilinks. (1 year, 3 months ago) <Bridger Maxwell>
    * |   81bf613 - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <benjaoming>
    |\ \  
    | * | 7aab68a - Adding ideas section. (1 year, 3 months ago) <benjaoming>
    * | | bb87802 - unchanged, git detects change but shows no diff (1 year, 3 months ago) <benjaoming>
    * | | 0fc9b2d - Important fix! Remove HTML tags from Markdown code. (1 year, 3 months ago) <benjaoming>
    * | | 4a58ac1 - Adding clearfix (1 year, 3 months ago) <benjaoming>
    |/ /  
    * | 98aaee3 - Issue #32, yes, clearly a typo here. Don't know why it was working, but replaced with super(RevisionForm.. and tested. (1 year, 3 months ago) <benjaoming>
    * |   7435980 - Merge pull request #35 from rfurman/master (1 year, 3 months ago) <benjaoming>
    |\ \  
    | * | 60142fa - Fixed image captions by resetting caption_lines for each new image.  Before, the n-th image would have the first n captions concatenated together. (1 year, 3 months ago) <Ralph Furmaniak>
    |/ /  
    * |   60c83ee - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <Bridger Maxwell>
    |\ \  
    | * | d9518ea - Only mark shown notifications as read -- never the ones that haven't been display because only 10 notifications are display at the same time... (1 year, 3 months ago) <benjaoming>
    | * | ebfaff4 - order notifications (1 year, 3 months ago) <benjaoming>
    | * | e229819 - Notify dropdown should look at the latest id of a notification and not retrieve any older notifications on updating from JSON. (1 year, 3 months ago) <benjaoming>
    | * | 288e25a - Merge user menu and notifications menu (1 year, 3 months ago) <benjaoming>
    | * | 3c9c2f1 - more search layout (1 year, 3 months ago) <benjaoming>
    | * |   6d20678 - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <benjaoming>
    | |\ \  
    | * | | f8a6e1c - Search "optimization".... layout-wise :) (1 year, 3 months ago) <benjaoming>
    * | | | a558ea6 - Allowing periods in slug for wikilinks. (1 year, 3 months ago) <Bridger Maxwell>
    | |/ /  
    |/| |   
    * | | 7f820b6 - user.is_superuser is not a function. (1 year, 3 months ago) <Bridger Maxwell>
    |/ /  
    * |   0012481 - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <benjaoming>
    |\ \  
    | |/  
    | * 63003aa - Removed print statement accidentally left in. (1 year, 3 months ago) <Bridger Maxwell>
    | * afdd97d - Made a workaround for django bug 15040, which made permissions forms have all checked boxes. (1 year, 3 months ago) <Bridger Maxwell>
    | * 6ccd08e - Moved subtree delete to a model method with transactions. (1 year, 3 months ago) <Bridger Maxwell>
    * | c0d7e2a - Search function (1 year, 3 months ago) <benjaoming>
    |/  
    * c2cfcc2 - A few search related things... adding search bar (doesnt work yet) (1 year, 3 months ago) <benjaoming>
    * 56d8e57 - Filtering on Directory listings. Issue #27 - never create a merged revision that inherits the deleted or locked attribute. (1 year, 3 months ago) <benjaoming>
    * 2979c98 - Few things here and there in the README (1 year, 3 months ago) <benjaoming>
    * ff8fd1c - Issue #28 (1 year, 3 months ago) <benjaoming>
    *   bf0d9cd - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <benjaoming>
    |\  
    | * 9865b5c - Changed preview to show warning when previewing a deleted revision. (1 year, 3 months ago) <Bridger Maxwell>
    | * d2f08a3 - You can now preview deleted revisions (so they work in the history tab). (1 year, 3 months ago) <Bridger Maxwell>
    | * a8dbb5f - Fixed confusing if statement that had the side effect of restoring every deleted article a moderator views. (1 year, 3 months ago) <Bridger Maxwell>
    | *   c432574 - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <Bridger Maxwell>
    | |\  
    | * | 1415c85 - Was accidentally using old permission for showing purge confirm form. (1 year, 3 months ago) <Bridger Maxwell>
    * | | b03a317 - Very small commit before merge... (1 year, 3 months ago) <benjaoming>
    * | | 8e691c1 - Modal should not animate... the bootstrap animation is loo choppy (1 year, 3 months ago) <benjaoming>
    | |/  
    |/|   
    * |   6be6a0c - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <benjaoming>
    |\ \  
    | |/  
    | *   32416cd - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <Bridger Maxwell>
    | |\  
    | * | ce4fd7a - Removed the lost and found until it can be debugged. (1 year, 3 months ago) <Bridger Maxwell>
    | * | 4ddc7cb - Properly deletes children when purging articles. (1 year, 3 months ago) <Bridger Maxwell>
    | * |   632bb59 - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <Bridger Maxwell>
    | |\ \  
    | * \ \   096e149 - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <Bridger Maxwell>
    | |\ \ \  
    | * \ \ \   af0b2a6 - Merge branch 'edx_release' (1 year, 3 months ago) <Bridger Maxwell>
    | |\ \ \ \  
    | | * | | | 82806fa - An article is now considered deleted if a parent is instead of explicitly needing to mark all children as deleted. (1 year, 3 months ago) <Bridger Maxwell>
    | | * | | | 02275fb - Fixed import for installation to run without attachments being enabled. (1 year, 3 months ago) <Bridger Maxwell>
    * | | | | | 915260d - oops mess (1 year, 3 months ago) <benjaoming>
    | |_|_|_|/  
    |/| | | |   
    * | | | | 59ecabd - Layout stuff (1 year, 3 months ago) <benjaoming>
    * | | | | 2770ad1 - Fix slug checking: Should respect case sensitivity (if configured) and feedback if its a deleted article (1 year, 3 months ago) <benjaoming>
    | |_|_|/  
    |/| | |   
    * | | | 66f357e - Removing the stupid delete check once and for all (1 year, 3 months ago) <benjaoming>
    | |_|/  
    |/| |   
    * | | d5d90a4 - Removing circular permission check can_write->can_delete->can_write.... (1 year, 3 months ago) <benjaoming>
    * | | a3ee89d - Adding user_can_read as a kwarg on Article.get_children (1 year, 3 months ago) <benjaoming>
    |/ /  
    * | 489dcba - Removing the is_moderator decorator -- it is replaced by can_moderate (1 year, 3 months ago) <benjaoming>
    * | 9a996a7 - Updating todo and comments (1 year, 3 months ago) <benjaoming>
    * |   1e5bb80 - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <benjaoming>
    |\ \  
    | * \   221fca1 - Merge branch 'edx_release' (1 year, 3 months ago) <Bridger Maxwell>
    | |\ \  
    | | |/  
    | | * 876357a - Added an error page (for when even the parent isn't found). (1 year, 3 months ago) <Bridger Maxwell>
    * | | 832d790 - Loads of changes in permission system. Many aspects are now configurable. (1 year, 3 months ago) <benjaoming>
    |/ /  
    * | 495d70e - Adding a couple of new settings that are not fully implemented yet. Do not let MARKDOWN_EXTENSIONS be a callable since the markdown_instance already has an article property accessible to any extension that wants it. (1 year, 3 months ago) <benjaoming>
    * | 9392b2f - Image deletion: Purge function to throw out files and everything! (1 year, 3 months ago) <benjaoming>
    * | 72a2884 - Update TODO. Should allow null values of image width and height since image files disappear sometimes and fields have to be emptied. (1 year, 3 months ago) <benjaoming>
    * | 46c4857 - Image captions should keep line breaks. Missing image files still keep causing problems (1 year, 3 months ago) <benjaoming>
    * | 5b49a60 - Fix whitespaces added from html template (1 year, 3 months ago) <benjaoming>
    * | 5352792 - Locking of articles and source view. (1 year, 3 months ago) <benjaoming>
    * | 8b4f51b - Settings tab should inherit from article.html (1 year, 3 months ago) <benjaoming>
    * | 4d941f6 - View Source is almost finished... (1 year, 3 months ago) <benjaoming>
    * | 4287c93 - Updates relating to new bootstrap version. Removing several js plugins as they are now in the minified bootstrap.js (1 year, 3 months ago) <benjaoming>
    * | 65147c5 - Inherit correct properties from predecessor and be more robust when returning size and filename on images (1 year, 3 months ago) <benjaoming>
    * | 657831f - IOError, not OSError (1 year, 3 months ago) <benjaoming>
    * | fabea44 - Add image.null=True for images field so that files can disappear and not cause unreparable error. (1 year, 3 months ago) <benjaoming>
    * | 471f8eb - Image replacement bug, did not inherit from predecessor (1 year, 3 months ago) <benjaoming>
    * | bff93ef - Updating test database (1 year, 3 months ago) <benjaoming>
    * | b4c18cb - Update to Bootstrap 2.1.0 (1 year, 3 months ago) <benjaoming>
    * | b39f8f1 - Printer friendliness (1 year, 3 months ago) <benjaoming>
    * | f9130a6 - Various small fixes (1 year, 3 months ago) <benjaoming>
    * | 1a4ef5a - Add links plugin to testproject. Do not fail if an attachment file has disappeared. (1 year, 3 months ago) <benjaoming>
    * | 2b8c7f4 - Adding a plugin for handling links and detecting if they are broken (which will show a read link in the article text). Also a sidebar for looking up links with typeahead. (1 year, 3 months ago) <benjaoming>
    |/  
    * e237b2a - Creating a proper WikiSlug javascript generator from the django urlify (1 year, 3 months ago) <benjaoming>
    *   95d8651 - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <benjaoming>
    |\  
    | * a49b4d5 - Patch for django bug where EmptyQuerySet actually needs the model to be set (or it can't raise a DoesNotExist exception). (1 year, 3 months ago) <Bridger Maxwell>
    * | 354c6b2 - Customizable storage backend for attachments. Proper error handling for illegal file types on replace view. (1 year, 3 months ago) <benjaoming>
    |/  
    * 7216584 - Browsing levels and adding articles to either current or parent level so users dont get confused about the hierarchy (1 year, 3 months ago) <benjaoming>
    * c83ad43 - Checking read permissions on page list (1 year, 3 months ago) <benjaoming>
    * b37e140 - Move add_select_related so it isn't a class method but an instance method of the URLPath's querysets. Fix error in permission lookup of users in a group. (1 year, 3 months ago) <benjaoming>
    * 0a273ee - Forgot a file in last commit, list.html (1 year, 3 months ago) <Bridger Maxwell>
    *   92ab132 - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <Bridger Maxwell>
    |\  
    | * 5988130 - Sidebar to handle plugins without a form (1 year, 3 months ago) <benjaoming>
    | * cd60dfd - Removing after refactor (1 year, 3 months ago) <benjaoming>
    | * 8d7f606 - Adding a help plugin and extra markdown extensions (1 year, 3 months ago) <benjaoming>
    | * 1b69061 - Permissions in settings tab can be applied recursively and owner can be changed. (1 year, 3 months ago) <benjaoming>
    | *   85c58dc - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <benjaoming>
    | |\  
    | * | 3edd286 - Adding possibility for Plugins to add media to rendering pages. Adding advanced markdown extension for images. Adding colorbox for images plugin to enlarge photos. (1 year, 3 months ago) <benjaoming>
    * | | 2edd8d3 - Added simple child list page. Doesn't have any styling yet. (1 year, 3 months ago) <Bridger Maxwell>
    | |/  
    |/|   
    * | 2d7c987 - children_slice is no longer queried when SHOW_MAX_CHILDREN=0 (1 year, 3 months ago) <Bridger Maxwell>
    * | 55469f7 - Further reducing sql queries. (1 year, 3 months ago) <Bridger Maxwell>
    * | 7c6af7b - Added caching of ancestors for urlpath to reduce sql queries. (1 year, 3 months ago) <Bridger Maxwell>
    |/  
    * df4fd06 - Sending request object to sidebar forms (1 year, 3 months ago) <benjaoming>
    * 7c1542c - Adding new image revisions and better looks for history page (1 year, 3 months ago) <benjaoming>
    * fcc466d - Image management, revert, delete and restore (1 year, 3 months ago) <benjaoming>
    * c145596 - Refactoring wiki.core.plugins (1 year, 3 months ago) <benjaoming>
    *   ebe86a4 - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <benjaoming>
    |\  
    | * 97f8413 - Fixed some circular imports that were causing errors. (1 year, 3 months ago) <Bridger Maxwell>
    | * 8e76eae - IMPORTANT: Fix this. I just commented out a line that was causing trouble. (1 year, 3 months ago) <Bridger Maxwell>
    | * 96328e3 - Changed getting of EditorClass and editor to functions (so they don't run so early). (1 year, 3 months ago) <Bridger Maxwell>
    * | 45b67b2 - Adding RevisionPlugin. Images plugin becoming a plugin with its own revision system. Fixing anonymous settings for attachments plugin. (1 year, 3 months ago) <benjaoming>
    |/  
    *   d58dcbc - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <Bridger Maxwell>
    |\  
    | * 1438944 - Moving sidebar outside of the main edit form so plugins can handle their own form data independently (1 year, 3 months ago) <benjaoming>
    * | 0072871 - Removed debug print. (1 year, 3 months ago) <Bridger Maxwell>
    |/  
    * eea5726 - Changing plugin base models for a more intuitive understanding of what types of models should exist. The image model should maintain revisions of itself to avoid a difficult process when replacing images. (1 year, 3 months ago) <benjaoming>
    * d4de685 - admin.py uses correct import of Editor, EditorClass. (1 year, 3 months ago) <Bridger Maxwell>
    * 12cc515 - Creating editors package with markitup module (1 year, 3 months ago) <benjaoming>
    * 8a7a3e7 - New app label for notifications (1 year, 3 months ago) <benjaoming>
    *   63b6da7 - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <benjaoming>
    |\  
    | * 95dd8fe - Moved MarkItUp editors to plugins also. (1 year, 3 months ago) <Bridger Maxwell>
    * | 8c84848 - comments (1 year, 3 months ago) <benjaoming>
    * | a4ef195 - New tables after altering APP_LABEL on plugins (1 year, 3 months ago) <benjaoming>
    |/  
    * d567a4d - Moving BaseEditor to wiki.plugins to avoid circular imports (1 year, 3 months ago) <benjaoming>
    *   944075a - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <benjaoming>
    |\  
    | * 48a1377 - Fixed render_to_string parameter (context was being passed in without using 'context_instance' kwarg) (1 year, 3 months ago) <Bridger Maxwell>
    | *   7b6078b - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <Bridger Maxwell>
    | |\  
    | * | 7ec4943 - Small typo where I used ANONYMOUS instead of ANONYMOUS_WRITE. (1 year, 3 months ago) <Bridger Maxwell>
    * | | 9a04ef4 - Changing app_label for plugin models (1 year, 3 months ago) <benjaoming>
    | |/  
    |/|   
    * | ab7dc9a - Adding migrations for URLPath.article cache field Adding dependency on sorl-thumbnail (1 year, 3 months ago) <benjaoming>
    * |   3e7ddf6 - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <benjaoming>
    |\ \  
    | |/  
    | * 473fd5e - Added a permission denied page. (1 year, 3 months ago) <Bridger Maxwell>
    | * 3324ab0 - Added a permission denied page. (1 year, 3 months ago) <Bridger Maxwell>
    * | 1d3677b - prefetch and swap lookups such that path is always looked up before article_id (1 year, 3 months ago) <benjaoming>
    * |   6af3dcb - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <benjaoming>
    |\ \  
    | |/  
    | * 8cd2bb7 - ANONYMOUS and ANONYMOUS_WRITE settings are now respected. (1 year, 3 months ago) <Bridger Maxwell>
    | * 9c83dfb - Fixed issues where 'if user.is_anonymous' was missing () so was always True (1 year, 3 months ago) <Bridger Maxwell>
    | * 484ff1c - Added auto migration. (1 year, 3 months ago) <Bridger Maxwell>
    | * cdb2c3a - Added a bit of caching to retrieving path, so it doesn't make so many sql queries. (1 year, 3 months ago) <Bridger Maxwell>
    | * 6c9e1a0 - Added a hack to the hacky reverse to allow for transforms on reversed url. (1 year, 3 months ago) <Bridger Maxwell>
    * | 5fe706c - Merging with Basecamp feature list (1 year, 3 months ago) <benjaoming>
    |/  
    *   4ab9701 - Merge branch 'master' of git://github.com/benjaoming/django-wiki (1 year, 3 months ago) <Bridger Maxwell>
    |\  
    | * b85791d - Message after uploading image. Do not redirect after plugin form submit as changes to article text and title are lost. (1 year, 3 months ago) <benjaoming>
    | * 0863c41 - Sidebar plugins. First plugin: images. Upload an image directly via a plugin on the edit page. (1 year, 3 months ago) <benjaoming>
    | * 6eae1fc - Instructions about settings and tips (1 year, 3 months ago) <benjaoming>
    | * 3a876d9 - Block anonymous access to upload files (1 year, 3 months ago) <benjaoming>
    * | c053503 - Added login_required to create_root. (1 year, 3 months ago) <Bridger Maxwell>
    * |   d238020 - Merge branch 'master' of git://github.com/benjaoming/django-wiki (1 year, 3 months ago) <Bridger Maxwell>
    |\ \  
    | |/  
    | * d1f50d1 - test db not properly synced (1 year, 3 months ago) <benjaoming>
    | * 19716f7 - Adding South migrations for wiki, django_notify and wiki plugins (1 year, 3 months ago) <benjaoming>
    | * a1d6ebe - Refactor plugins: Put base classes in wiki.plugins (1 year, 3 months ago) <benjaoming>
    | * f7f6527 - Deleted article view with purge and restore options (1 year, 3 months ago) <benjaoming>
    | * 63c7e9f - Correctly inform user that a deletion ALSO deletes children. (1 year, 3 months ago) <benjaoming>
    | * 8ce2236 - Deletion for articles: Soft delete and purge. Also soft deletes or purges children. A soft deletion creates a new revision in which the article is marked as deleted. (1 year, 3 months ago) <benjaoming>
    | * c1514ab - Do not delete old notifications when user unsubscribes + allow notifications to be created without a subscription (to enable notifications for only one specific user) (1 year, 3 months ago) <benjaoming>
    | * 4800d5b - Decorator for muting notifications + Issue #11 fix (1 year, 3 months ago) <benjaoming>
    | * 2eae064 - Correcting errors caused by removal of Article.title field. Almost done with Delete view. (1 year, 3 months ago) <benjaoming>
    * | c10ee82 - Corrected parameters on render_to_response. Also fixed login url resolution when ACCOUNT_HANDLING=False. (1 year, 3 months ago) <Bridger Maxwell>
    * |   9f1b3a9 - Merge branch 'master' of git://github.com/benjaoming/django-wiki (1 year, 3 months ago) <Bridger Maxwell>
    |\ \  
    | |/  
    | * c3303e1 - Example urlpattern Issue #12 (1 year, 3 months ago) <benjaoming>
    | * 84d44da - Updating week and date (1 year, 3 months ago) <benjaoming>
    | * 0303bcd - Headlines (1 year, 3 months ago) <benjaoming>
    | * 0de3382 - Nicer headlines for install instructions (1 year, 3 months ago) <benjaoming>
    | * 5710402 - Small things (1 year, 3 months ago) <benjaoming>
    | * 11b00ec - Adding mptt to requirements Issue #10 (1 year, 3 months ago) <benjaoming>
    | * 869a62e - Better install instructions for Issue #14 and #12 (1 year, 3 months ago) <benjaoming>
    | *   43c32df - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 3 months ago) <benjaoming>
    | |\  
    | | *   1888ff6 - Merge pull request #15 from hgdeoro/updates-on-readme (1 year, 3 months ago) <benjaoming>
    | | |\  
    | | | * 212b3a2 - Updated install instructions on README. (1 year, 3 months ago) <Horacio G. de Oro>
    | | * |   f365669 - Merge pull request #10 from hgdeoro/pip-requirements (1 year, 3 months ago) <benjaoming>
    | | |\ \  
    | | | * | 0b054e0 - README: added instructions: how to use requirements.txt to install dependencies. (1 year, 3 months ago) <Horacio G. de Oro>
    | | | * | 5e5640f - Creates a requirements.txt to facilitate installing dependencies. (1 year, 3 months ago) <Horacio G. de Oro>
    | | | |/  
    | * | | 94a3ebf - Remove redundant Article.title field (1 year, 3 months ago) <benjaoming>
    | * | | 4418482 - Making footer prettier, clean up code (1 year, 3 months ago) <benjaoming>
    | |/ /  
    * | |   341db91 - Merge branch 'master' of git://github.com/benjaoming/django-wiki (1 year, 3 months ago) <Bridger Maxwell>
    |\ \ \  
    | |/ /  
    | * | 846a665 - Cleaning up template boiler plate markup (1 year, 3 months ago) <benjaoming>
    | * | 588bcdd - Making notifications update in a smart way. Fixing wrong urls in accounts (1 year, 3 months ago) <benjaoming>
    | * | bf09bf4 - Changing the urlpatterns to always prioritize paths over IDs if a path string is supplied -- even an empty one for the root article. Also modifying models in pluginbase to not be abstract such that it is possible to generically access all types of plugins. (1 year, 3 months ago) <benjaoming>
    | * | 33186aa - Adding model chart generation of the wiki (1 year, 3 months ago) <benjaoming>
    | |/  
    * |   193d514 - Merge branch 'master' of git://github.com/benjaoming/django-wiki (1 year, 3 months ago) <Bridger Maxwell>
    |\ \  
    | |/  
    | * afce7d8 - msg when child menu is empty (1 year, 4 months ago) <benjaoming>
    | * b3bf535 - msg when child menu is empty (1 year, 4 months ago) <benjaoming>
    | * 1bff649 - insert transaction commits so they cover all cases (1 year, 4 months ago) <benjaoming>
    | * 7091ac9 - Use chained QuerySet objects for can_read and can_write methods and active() to filter out inactive objects. Issue #9 (1 year, 4 months ago) <benjaoming>
    * | a7a5f5e - Added related_name to Article.owner to prevent conflict with existing Simplewiki install. (1 year, 3 months ago) <Bridger Maxwell>
    |/  
    * ea26ab8 - Anonymous users cannot be used in queries! (1 year, 4 months ago) <benjaoming>
    * c619639 - Making more agile url patterns that are agnostic to either receiving a  path or an article_id. The path takes precedence over the article_id, except for the root article which needs to be forced in the template. Prettyfying the article revision list. (1 year, 4 months ago) <benjaoming>
    * 24ea671 - Failed use of select_related -- need some good idea. Better UI with current level's child articles as dropdown menu. (1 year, 4 months ago) <benjaoming>
    * 2864d69 - Avoid duplicate notifications for overlapping subscription types. Make notification list empty when marking all notifications as read. (1 year, 4 months ago) <benjaoming>
    * b676975 - Admin labels (1 year, 4 months ago) <benjaoming>
    * b232ea8 - Notifications for attachments plugin and plugins in general (1 year, 4 months ago) <benjaoming>
    * 276c658 - Prettyfying the attachments page (1 year, 4 months ago) <benjaoming>
    * c385fc6 - Renaming permission - no permissions should overlap in their meaning. Fixing can_read and can_write on Article instances to match new permissions. (1 year, 4 months ago) <benjaoming>
    * efe01f7 - Improving managers. Adding select_related (untested) on get_article decorator. Adding search function for attachments to add other article's attachments. Adding better permission handling through managers. (1 year, 4 months ago) <benjaoming>
    * 6988059 - Fixing preview function to use correct revision id (1 year, 4 months ago) <benjaoming>
    * 299017e - Wrong preview link (1 year, 4 months ago) <benjaoming>
    * 19b191a - Removing files that should not be in testproject (1 year, 4 months ago) <benjaoming>
    * d264f48 - Further frustations perhaps fixed on file upload issues (1 year, 4 months ago) <benjaoming>
    * 751c21a - Better error if permissions are wrong on MEDIA_ROOT (1 year, 4 months ago) <benjaoming>
    * b6e7b94 - Hopefully fixing transaction issue for other systems (1 year, 4 months ago) <benjaoming>
    * 0c57d76 - moving transaction commit (1 year, 4 months ago) <benjaoming>
    * 08bfb16 - More robustness in Attachments plugin. Give a good error message upon non-allowed uploads. Fix JSON decorator error. Ignore media files in test project. (1 year, 4 months ago) <benjaoming>
    * a2ba2c8 - Attachment plugin almost finished. Can delete and restore files and replace. Contains a smart obscurification feature that hides files. This way, files can have reading restrictions imposed. (1 year, 4 months ago) <benjaoming>
    * d96da78 - Better install instructions (1 year, 4 months ago) <benjaoming>
    * 81e8157 - Simple account handling, log in, log out and sign up. (1 year, 4 months ago) <benjaoming>
    * bfef21b - A bit of login toolbar (1 year, 4 months ago) <benjaoming>
    * ebb25ab - Adding notify frontend. (1 year, 4 months ago) <benjaoming>
    * 1a0396d - Adding from old feature list (1 year, 4 months ago) <benjaoming>
    * 5e3b668 - Add GPLv3 license, clean up code (1 year, 4 months ago) <benjaoming>
    * 8408f01 - More class-based views. Mixin class for Article-related views handling permissions etc. More complex plugin structure for easy creation of plugins with very easy integration in the article tab menu etc. (1 year, 4 months ago) <benjaoming>
    * fa4af85 - Error on saving revisions for anonymous users (1 year, 4 months ago) <benjaoming>
    * 64a20e8 - Adding notifications for article edits and creations (1 year, 4 months ago) <benjaoming>
    * 700e466 - Fixing js bug in SelectWidgetBootstrap (1 year, 4 months ago) <benjaoming>
    * 4162909 - Fix Issue #7 (in setup.py) + Add forms in settings tab, save new permissions and notification preferences (1 year, 4 months ago) <benjaoming>
    * 15a363d - Detection of editing conflicts, ie. concurrent article edits. If the revision number has changed while editing, warn the user and merge the user's content with the new revision. (1 year, 4 months ago) <benjaoming>
    * 9d92e96 - Updating the TODO (1 year, 4 months ago) <benjaoming>
    * 68e6c32 - added text editor backup files to gitignore; fix url tags so they are django 1.3-style, so it works properly with django 1.5 (which requires it) (1 year, 4 months ago) <Michael Farrell>
    * 3500999 - django_notify in wiki self-check on INSTALLED_APPS and a better README.md (1 year, 4 months ago) <benjaoming>
    * acff0fe - Update django_notify/README (1 year, 4 months ago) <benjaoming>
    * 083b56d - Update README.md (1 year, 4 months ago) <benjaoming>
    * 9dda155 - Update README.md (1 year, 4 months ago) <benjaoming>
    * 56ef8e6 - Update README.md (1 year, 4 months ago) <benjaoming>
    * 4ede9c8 - Creating new notification application django_notify and adding support for plugin registration and hooking additional forms into the settings page, such as notification settings for articles. (1 year, 4 months ago) <benjaoming>
    * 99041d5 - Redirecting if article does not exist, add user and ip_address to new articles (1 year, 4 months ago) <benjaoming>
    * efd542a - Create function added (1 year, 4 months ago) <benjaoming>
    * b75d893 - Diffs also display log messages and title changes (1 year, 4 months ago) <benjaoming>
    * 37b1cd5 - Pressing the final merge button now works and puts an automatic log entry (1 year, 4 months ago) <benjaoming>
    *   83394ad - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 4 months ago) <benjaoming>
    |\  
    | * 9360e1d - Update README.md (1 year, 4 months ago) <benjaoming>
    | * dc3e415 - Update README.md (1 year, 4 months ago) <benjaoming>
    * | e19ec3a - Viewing diffs and merging revisions. (1 year, 4 months ago) <benjaoming>
    |/  
    * 327ff0c - Issue #4 and #2 (1 year, 4 months ago) <benjaoming>
    *   06d06ce - Merge branch 'master' of github.com:benjaoming/django-wiki (1 year, 4 months ago) <benjaoming>
    |\  
    | * b096e34 - Update README.md (1 year, 4 months ago) <benjaoming>
    | * 60bc647 - Adding sekizai dep. (1 year, 4 months ago) <benjaoming>
    * | 750f6b4 - Adding history page, first class-based view, saving pointer to previous revision, better more strict handling of URLS (must always end with a /, except the root which must be "") (1 year, 4 months ago) <benjaoming>
    |/  
    * 8294826 - A few deployment details (1 year, 4 months ago) <benjaoming>
    * 58cf1a3 - Adding edit page, preview function and MORE. South migrations will be added back soon. (1 year, 4 months ago) <benjaoming>
    * dba6f82 - Adding template tags, bootstrap front end, creation of first root article, template tags for rendering (1 year, 4 months ago) <benjaoming>
    * 458bbd2 - Initial plugin and editor structure and base classes for extending MarkItUp editor in admin Creating images and attachments as plugins (1 year, 4 months ago) <benjaoming>
    * 2940142 - More work on models. Add Attachment model, and let attachments pass through a revision system. (1 year, 4 months ago) <benjaoming>
    * 322b5a6 - Finalizing URLPath as an MPTT model and generic relations on Articles (1 year, 4 months ago) <benjaoming>
    * 83fe3d4 - More on models. Not done yet. (1 year, 4 months ago) <benjaoming>
    * 30fb1ec - Begging to implement models (1 year, 4 months ago) <benjaoming>
    * 330c772 - Django south administration and URL patterns with default namespace (1 year, 4 months ago) <benjaoming>
    * ef2b1ec - Documentation with sphinx (1 year, 4 months ago) <benjaoming>
    * 357d9fa - Adding install instructions and setup.py (1 year, 4 months ago) <benjaoming>
    * 692aeae - Prepopulated test project. (1 year, 4 months ago) <benjaoming>
    * a3fe227 - typos (1 year, 4 months ago) <benjaoming>
    * 0e24a0b - typos (1 year, 4 months ago) <benjaoming>
    * de6c30b - Project skeleton, README with explanation of project (1 year, 4 months ago) <benjaoming>
    * aac85a2 - Update master (1 year, 4 months ago) <benjaoming>
    * ad97277 - Initial commit (1 year, 4 months ago) <benjaoming>