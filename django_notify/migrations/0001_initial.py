# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NotificationType'
        db.create_table('notify_notificationtype', (
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128, primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
        ))
        db.send_create_signal('django_notify', ['NotificationType'])

        # Adding model 'Settings'
        db.create_table('notify_settings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('interval', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal('django_notify', ['Settings'])

        # Adding model 'Subscription'
        db.create_table('notify_subscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('settings', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_notify.Settings'])),
            ('notification_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_notify.NotificationType'])),
            ('object_id', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('send_emails', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('django_notify', ['Subscription'])

        # Adding model 'Notification'
        db.create_table('notify_notification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subscription', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_notify.Subscription'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('is_viewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_emailed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('django_notify', ['Notification'])


    def backwards(self, orm):
        # Deleting model 'NotificationType'
        db.delete_table('notify_notificationtype')

        # Deleting model 'Settings'
        db.delete_table('notify_settings')

        # Deleting model 'Subscription'
        db.delete_table('notify_subscription')

        # Deleting model 'Notification'
        db.delete_table('notify_notification')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
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
        'django_notify.notification': {
            'Meta': {'object_name': 'Notification', 'db_table': "'notify_notification'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_emailed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_notify.Subscription']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'django_notify.notificationtype': {
            'Meta': {'object_name': 'NotificationType', 'db_table': "'notify_notificationtype'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'django_notify.settings': {
            'Meta': {'object_name': 'Settings', 'db_table': "'notify_settings'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'django_notify.subscription': {
            'Meta': {'object_name': 'Subscription', 'db_table': "'notify_subscription'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notification_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_notify.NotificationType']"}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'send_emails': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'settings': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_notify.Settings']"})
        }
    }

    complete_apps = ['django_notify']