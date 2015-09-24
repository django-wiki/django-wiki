# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ("django_nyt", "0001_initial"),
    )

    def forwards(self, orm):
        # Adding model 'ArticleSubscription'
        db.create_table('notifications_articlesubscription', (
            ('articleplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(primary_key=True, to=orm['wiki.ArticlePlugin'], unique=True)),
            ('subscription', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['django_nyt.Subscription'], unique=True)),
        ))
        db.send_create_signal('notifications', ['ArticleSubscription'])

        # Adding unique constraint on 'ArticleSubscription', fields ['subscription', 'articleplugin_ptr']
        db.create_unique('notifications_articlesubscription', ['subscription_id', 'articleplugin_ptr_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ArticleSubscription', fields ['subscription', 'articleplugin_ptr']
        db.delete_unique('notifications_articlesubscription', ['subscription_id', 'articleplugin_ptr_id'])

        # Deleting model 'ArticleSubscription'
        db.delete_table('notifications_articlesubscription')


    # Some model definitions have been truncated to avoid referencing
    # auth.User. South only really needs to know the full definition of models
    # in this app, plus the names of a few other tables, not everything they are
    # related to.

    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'django_nyt.subscription': {
            'Meta': {'db_table': "'nyt_subscription'", 'object_name': 'Subscription'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        },
        'notifications.articlesubscription': {
            'Meta': {'object_name': 'ArticleSubscription', '_ormbases': ['wiki.ArticlePlugin'], 'unique_together': "(('subscription', 'articleplugin_ptr'),)"},
            'articleplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'to': "orm['wiki.ArticlePlugin']", 'unique': 'True'}),
            'subscription': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['django_nyt.Subscription']", 'unique': 'True'})
        },
        'wiki.articleplugin': {
            'Meta': {'object_name': 'ArticlePlugin'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
    }

    complete_apps = ['notifications']
