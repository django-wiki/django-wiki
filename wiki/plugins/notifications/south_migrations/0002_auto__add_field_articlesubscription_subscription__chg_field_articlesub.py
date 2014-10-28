from __future__ import absolute_import
from __future__ import unicode_literals
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

user_orm_label = '%s.%s' % (User._meta.app_label, User._meta.object_name)
user_model_label = '%s.%s' % (User._meta.app_label, User._meta.module_name) 


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ArticleSubscription.subscription'
        db.add_column('notifications_articlesubscription', 'subscription',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['django_nyt.Subscription'], unique=True, null=True),
                      keep_default=False)


        # Renaming column for 'ArticleSubscription.subscription_ptr' to match new field type.
        # db.rename_column(u'notifications_articlesubscription', 'subscription_ptr_id', u'subscription_ptr')
        # Changing field 'ArticleSubscription.subscription_ptr'
        # db.alter_column(u'notifications_articlesubscription', u'subscription_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, db_column=u'subscription_ptr', to=orm['django_nyt.Subscription']))

    def backwards(self, orm):
        # Deleting field 'ArticleSubscription.subscription'
        db.delete_column('notifications_articlesubscription', 'subscription_id')

        # Renaming column for 'ArticleSubscription.subscription_ptr' to match new field type.
        #  db.rename_column(u'notifications_articlesubscription', u'subscription_ptr', 'subscription_ptr_id')
        # Changing field 'ArticleSubscription.subscription_ptr'
        # db.alter_column(u'notifications_articlesubscription', 'subscription_ptr_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['django_notify.Subscription'], unique=True))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        user_model_label: {
            'Meta': {'object_name': User.__name__, 'db_table': "'%s'" % User._meta.db_table},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'django_nyt.notification': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'Notification', 'db_table': "'nyt_notification'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_emailed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'occurrences': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_nyt.Subscription']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'django_nyt.notificationtype': {
            'Meta': {'object_name': 'NotificationType', 'db_table': "'nyt_notificationtype'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'django_nyt.settings': {
            'Meta': {'object_name': 'Settings', 'db_table': "'nyt_settings'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s']" % user_orm_label})
        },
        'django_nyt.subscription': {
            'Meta': {'object_name': 'Subscription', 'db_table': "'nyt_subscription'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'latest_for'", 'null': 'True', 'to': "orm['django_nyt.Notification']"}),
            'notification_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_nyt.NotificationType']"}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'send_emails': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'settings': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_nyt.Settings']"})
        },
        'notifications.articlesubscription': {
            'Meta': {'object_name': 'ArticleSubscription', '_ormbases': ['wiki.ArticlePlugin']},
            'articleplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['wiki.ArticlePlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'subscription': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['django_nyt.Subscription']", 'unique': 'True', 'null': 'True'}),
            'subscription_ptr': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'deprecated_subscriptions'", 'unique': 'True', 'db_column': "u'subscription_ptr'", 'to': "orm['django_nyt.Subscription']"})
        },
        'wiki.article': {
            'Meta': {'object_name': 'Article'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_revision': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "u'current_set'", 'unique': 'True', 'null': 'True', 'to': "orm['wiki.ArticleRevision']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Group']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'group_read': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'group_write': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'other_read': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'other_write': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'owned_articles'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['%s']" % user_orm_label})
        },
        'wiki.articleplugin': {
            'Meta': {'object_name': 'ArticlePlugin'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.Article']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'wiki.articlerevision': {
            'Meta': {'ordering': "(u'created',)", 'unique_together': "((u'article', u'revision_number'),)", 'object_name': 'ArticleRevision'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.Article']"}),
            'automatic_log': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'previous_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.ArticleRevision']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'revision_number': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s']" % user_orm_label, 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'user_message': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['notifications']