# Contributing

If you are a developer, please refer to the
[Developer Guide](http://django-wiki.readthedocs.io/en/latest/development/index.html)

## Support

**DO NOT USE GITHUB FOR SUPPORT INQUIRIES! USE IRC OR MAILING LIST!**

Django-wiki is community based, please try to be active. If you want help, plan
to give help, too. For instance, if you join IRC, then stay around and help
others.

## Issues

Contributions are appreciated! The following guide is a rough draft, but
please feel free to contribute to this contribution doc as well :D

When submitting an Issue, please provide the following:

* If it's a **feature request**, then write why *you* want it, but also which other
  cases you find it useful for. Best way to get a new feature made by others
  is to motivate.
  * Think about challenges.
  * Have you read the Manifesto (below) ? New features should maintain the focus
    of the project.
* If you encounter a **bug**, keep in mind that it's probably easiest to fix if
  a developer sat in front of your computer... but in lack of that option:
  * `django-admin.py --version`
  * `python --version`
  * `uname -a`
  * An example of how to reproduce the bug.
  * The expected result.
  * Does the bug happen with a checkout of django-wiki's master branch? To upgrade:
    `pip install --upgrade git+https://github.com/django-wiki/django-wiki.git`

## Manifesto

Django needs a mature wiki system appealing to all kinds of needs, both big and small:

 * **Be pluggable and light-weight.** Don't integrate optional features in the core.
 * **Be open.** Make an extension API that allows the ecology of the wiki to grow. After all, Wikipedia consists of some [680 extensions](http://svn.wikimedia.org/viewvc/mediawiki/trunk/extensions/) written for MediaWiki.
 * **Be smart.** [This is](https://upload.wikimedia.org/wikipedia/commons/8/88/MediaWiki_database_schema_1-19_%28r102798%29.png) the map of tables in MediaWiki - we'll understand the choices of other wiki projects and make our own. After-all, this is a Django project.
 * **Be simple.** The source code should *almost* explain itself.
 * **Be structured.** Markdown is a simple syntax for readability. Features should be implemented either through easy coding patterns in the content field, but rather stored in a structured way (in the database) and managed through a friendly interface. This gives control back to the website developer, and makes knowledge more usable. Just ask: Why has Wikipedia never changed? Answer: Because it's knowledge is stored in a complicated way, thus it becomes very static.
