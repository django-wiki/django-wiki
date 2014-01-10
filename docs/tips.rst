Other tips
==========

1. **Account handling:** There are simple views that handle login,
   logout and signup. They are on by default. Make sure to set
   ``settings.LOGIN_URL`` to point to your login page as many wiki views
   may redirect to a login page.

2. **Syntax highlighting:** Python-Markdown has a pre-shipped codehilite
   extension which works perfectly, so add something like::

       WIKI_MARKDOWN_KWARGS = {'extensions': ['footnotes', 'attr_list', 'headerid', 'extra', 'codehilite', ]}

   to your settings. Currently, django-wiki shippes with a stylesheet
   that already has the syntax highlighting CSS rules built-in. Oh, and
   you need to ensure ``pip install pygments`` because Pygments is what
   the codehilite extension is using!
