# -*- coding: utf-8 -*-
"""Refactor South migrations to use settings.AUTH_USER_MODEL.
Inserts a backwards-compatible code-snippet in all
your schema migration files and uses a possibly customized user
model as introduced in Django 1.5.

Please note that this has nothing to do with changing
settings.AUTH_USER_MODEL to a new model. If you do this, stuff
will very likely break in reusable apps that have their own
migration trees.

Attributions:
github "benjaoming" this script

github "rockymeza" for this commit which held the ingredients:
https://github.com/fusionbox/mezzanine/commit/a9ea14719ad70ef2c92b26162eb3ae90283dbea2

Stackexchange Q&A:
http://stackoverflow.com/questions/15472704/trouble-migrating-reusable-django-app-models-to-use-a-custom-user-model

Usage:
  custom_user_auth_south_refactor.py <migration-dir>
  custom_user_auth_south_refactor.py (-h | --help)
  custom_user_auth_south_refactor.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from docopt import docopt
import os
import re

RE_CLASS_NAME = re.compile(r'^()^(class\s+Migration\s*\(\s*(SchemaMigration|DataMigration)\s*\)\s*:)', 
    re.MULTILINE)

INSERT_AT_TOP_OF_MIGRATION = """try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

user_orm_label = '%s.%s' % (User._meta.app_label, User._meta.object_name)
user_model_label = '%s.%s' % (User._meta.app_label, User._meta.model_name if hasattr(User._meta, 'model_name') else User._meta.module_name)


"""
RE_FK_LABEL = re.compile(r"to\=orm\[\'auth\.User\'\]")
RE_FK_LABEL_TO = "to=orm[user_orm_label]"

RE_FK_BACKWARDS = re.compile(r"'to':\s*\"orm\['auth\.User'\]\"")
RE_FK_BACKWARDS_TO = "'to': \"orm['%s']\" % user_orm_label"

RE_AUTH_MODEL = re.compile(r"'auth\.user'\:\s*\{")
RE_AUTH_MODEL_TO = r"user_model_label: {"

RE_META_STRING = re.compile(r"'Meta':\s*\{\s*'object_name'\s*:\s*'User'\s*\}")
RE_META_TO = "'Meta': {'object_name': User.__name__, 'db_table': \"'%s'\" % User._meta.db_table}"

RE_TEST_OK = re.compile(r"'auth.User'", re.IGNORECASE)

RE_MIGRATION_FNAME = re.compile(r"^(\d{4}).+py$")

if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.0')
    migration_dir = arguments['<migration-dir>']
    for fname in os.listdir(migration_dir):
        if not RE_MIGRATION_FNAME.search(fname):
            continue
        full_path = os.path.join(migration_dir, fname)
        f = open(full_path, 'r')
        contents = f.read()
        f.close()
        if RE_FK_LABEL.search(contents) or RE_META_STRING.search(contents) or RE_AUTH_MODEL.search(contents) or RE_FK_LABEL.search(contents):
            print("Refactoring {0}".format(fname))
            f = open(full_path, 'w')
            contents = RE_CLASS_NAME.sub(INSERT_AT_TOP_OF_MIGRATION + r"\2", 
                contents)
            contents = RE_AUTH_MODEL.sub(RE_AUTH_MODEL_TO, contents)
            contents = RE_META_STRING.sub(RE_META_TO, contents)
            contents = RE_FK_BACKWARDS.sub(RE_FK_BACKWARDS_TO, contents)
            contents = RE_FK_LABEL.sub(RE_FK_LABEL_TO, contents)
            f.write(contents)
            f.close()
        else:
            print("Skipping {0}".format(fname))            
        if RE_TEST_OK.search(contents):
            print("    WARNING! Still found occurrences of auth.User. Fix manually!")
