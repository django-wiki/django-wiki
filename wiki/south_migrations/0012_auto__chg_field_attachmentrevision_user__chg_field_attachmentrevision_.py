from __future__ import absolute_import
from __future__ import unicode_literals
# -*- coding: utf-8 -*-
import datetime
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

        # Changing field 'AttachmentRevision.user'
        db.alter_column('wiki_attachmentrevision', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm[user_orm_label], null=True, on_delete=models.SET_NULL))

        # Changing field 'AttachmentRevision.file'
        db.alter_column('wiki_attachmentrevision', 'file', self.gf('django.db.models.fields.files.FileField')(max_length=255))

        # Changing field 'RevisionPluginRevision.user'
        db.alter_column('wiki_revisionpluginrevision', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm[user_orm_label], null=True, on_delete=models.SET_NULL))

        # Changing field 'ArticleRevision.user'
        db.alter_column('wiki_articlerevision', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm[user_orm_label], null=True, on_delete=models.SET_NULL))

        # Changing field 'Article.group'
        db.alter_column('wiki_article', 'group_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'], null=True, on_delete=models.SET_NULL))

        # Changing field 'Article.owner'
        db.alter_column('wiki_article', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm[user_orm_label]))

    def backwards(self, orm):

        # Changing field 'AttachmentRevision.user'
        db.alter_column('wiki_attachmentrevision', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm[user_orm_label], null=True))

        # Changing field 'AttachmentRevision.file'
        db.alter_column('wiki_attachmentrevision', 'file', self.gf('django.db.models.fields.files.FileField')(max_length=100))

        # Changing field 'RevisionPluginRevision.user'
        db.alter_column('wiki_revisionpluginrevision', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm[user_orm_label], null=True))

        # Changing field 'ArticleRevision.user'
        db.alter_column('wiki_articlerevision', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm[user_orm_label], null=True))

        # Changing field 'Article.group'
        db.alter_column('wiki_article', 'group_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'], null=True))

        # Changing field 'Article.owner'
        db.alter_column('wiki_article', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm[user_orm_label]))

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
        'django_notify.notification': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'Notification', 'db_table': "'notify_notification'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_emailed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'occurrences': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s']" % user_orm_label})
        },
        'django_notify.subscription': {
            'Meta': {'object_name': 'Subscription', 'db_table': "'notify_subscription'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'latest_for'", 'null': 'True', 'to': "orm['django_notify.Notification']"}),
            'notification_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_notify.NotificationType']"}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'send_emails': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'settings': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_notify.Settings']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'wiki.article': {
            'Meta': {'object_name': 'Article'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_revision': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'current_set'", 'unique': 'True', 'null': 'True', 'to': "orm['wiki.ArticleRevision']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Group']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'group_read': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'group_write': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'other_read': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'other_write': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owned_articles'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['%s']" % user_orm_label})
        },
        'wiki.articleforobject': {
            'Meta': {'unique_together': "(('content_type', 'object_id'),)", 'object_name': 'ArticleForObject'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.Article']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_articleforobject'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_mptt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'wiki.articleplugin': {
            'Meta': {'object_name': 'ArticlePlugin'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.Article']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'wiki.articlerevision': {
            'Meta': {'ordering': "('created',)", 'unique_together': "(('article', 'revision_number'),)", 'object_name': 'ArticleRevision'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.Article']"}),
            'automatic_log': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'previous_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.ArticleRevision']", 'null': 'True', 'blank': 'True'}),
            'revision_number': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s']" % user_orm_label, 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'user_message': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'wiki.articlesubscription': {
            'Meta': {'object_name': 'ArticleSubscription', '_ormbases': ['wiki.ArticlePlugin', 'django_notify.Subscription']},
            'articleplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['wiki.ArticlePlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'subscription_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['django_notify.Subscription']", 'unique': 'True'})
        },
        'wiki.attachment': {
            'Meta': {'object_name': 'Attachment', '_ormbases': ['wiki.ReusablePlugin']},
            'current_revision': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'current_set'", 'unique': 'True', 'null': 'True', 'to': "orm['wiki.AttachmentRevision']"}),
            'original_filename': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'reusableplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['wiki.ReusablePlugin']", 'unique': 'True', 'primary_key': 'True'})
        },
        'wiki.attachmentrevision': {
            'Meta': {'ordering': "('created',)", 'object_name': 'AttachmentRevision'},
            'attachment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.Attachment']"}),
            'automatic_log': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'previous_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.AttachmentRevision']", 'null': 'True', 'blank': 'True'}),
            'revision_number': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s']" % user_orm_label, 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'user_message': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'wiki.image': {
            'Meta': {'object_name': 'Image', '_ormbases': ['wiki.RevisionPlugin']},
            'revisionplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['wiki.RevisionPlugin']", 'unique': 'True', 'primary_key': 'True'})
        },
        'wiki.imagerevision': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'ImageRevision', '_ormbases': ['wiki.RevisionPluginRevision']},
            'height': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'revisionpluginrevision_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['wiki.RevisionPluginRevision']", 'unique': 'True', 'primary_key': 'True'}),
            'width': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'wiki.reusableplugin': {
            'Meta': {'object_name': 'ReusablePlugin', '_ormbases': ['wiki.ArticlePlugin']},
            'articleplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['wiki.ArticlePlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'articles': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'shared_plugins_set'", 'symmetrical': 'False', 'to': "orm['wiki.Article']"})
        },
        'wiki.revisionplugin': {
            'Meta': {'object_name': 'RevisionPlugin', '_ormbases': ['wiki.ArticlePlugin']},
            'articleplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['wiki.ArticlePlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'current_revision': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'plugin_set'", 'unique': 'True', 'null': 'True', 'to': "orm['wiki.RevisionPluginRevision']"})
        },
        'wiki.revisionpluginrevision': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'RevisionPluginRevision'},
            'automatic_log': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'plugin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revision_set'", 'to': "orm['wiki.RevisionPlugin']"}),
            'previous_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.RevisionPluginRevision']", 'null': 'True', 'blank': 'True'}),
            'revision_number': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s']" % user_orm_label, 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'user_message': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'wiki.simpleplugin': {
            'Meta': {'object_name': 'SimplePlugin', '_ormbases': ['wiki.ArticlePlugin']},
            'article_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.ArticleRevision']"}),
            'articleplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['wiki.ArticlePlugin']", 'unique': 'True', 'primary_key': 'True'})
        },
        'wiki.urlpath': {
            'Meta': {'unique_together': "(('site', 'parent', 'slug'),)", 'object_name': 'URLPath'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.Article']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['wiki.URLPath']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['wiki']
