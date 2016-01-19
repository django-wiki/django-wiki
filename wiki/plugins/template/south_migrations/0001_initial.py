# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Template'
        db.create_table('template_template', (
            ('reusableplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['wiki.ReusablePlugin'], unique=True, primary_key=True)),
            ('current_revision', self.gf('django.db.models.fields.related.OneToOneField')(
                blank=True, related_name='current_set', unique=True, null=True, to=orm['template.TemplateRevision'])),
            ('template_title', self.gf('django.db.models.fields.SlugField')
             (unique=True, max_length=50)),
            ('extend_to_children', self.gf(
                'django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('template', ['Template'])

        # Adding model 'TemplateRevision'
        db.create_table('template_templaterevision', (
            ('id', self.gf('django.db.models.fields.AutoField')
             (primary_key=True)),
            ('revision_number', self.gf(
                'django.db.models.fields.IntegerField')()),
            ('user_message', self.gf(
                'django.db.models.fields.TextField')(blank=True)),
            ('automatic_log', self.gf(
                'django.db.models.fields.TextField')(blank=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')
             (max_length=15, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(
                to=orm['auth.User'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')
             (auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')
             (auto_now_add=True, blank=True)),
            ('previous_revision', self.gf('django.db.models.fields.related.ForeignKey')(to=orm[
             'template.TemplateRevision'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')
             (default=False)),
            ('locked', self.gf('django.db.models.fields.BooleanField')
             (default=False)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['template.Template'])),
            ('template_content', self.gf(
                'django.db.models.fields.TextField')(blank=True)),
            ('description', self.gf(
                'django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('template', ['TemplateRevision'])

    def backwards(self, orm):
        # Deleting model 'Template'
        db.delete_table('template_template')

        # Deleting model 'TemplateRevision'
        db.delete_table('template_templaterevision')

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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'template.template': {
            'Meta': {'object_name': 'Template', '_ormbases': ['wiki.ReusablePlugin']},
            'current_revision': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'current_set'", 'unique': 'True', 'null': 'True', 'to': "orm['template.TemplateRevision']"}),
            'reusableplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['wiki.ReusablePlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'template_title': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'extend_to_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
        },
        'template.templaterevision': {
            'Meta': {'ordering': "('created',)", 'object_name': 'TemplateRevision'},
            'automatic_log': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'previous_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['template.TemplateRevision']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'revision_number': ('django.db.models.fields.IntegerField', [], {}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['template.Template']"}),
            'template_content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'user_message': ('django.db.models.fields.TextField', [], {'blank': 'True'})
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
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owned_articles'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"})
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
            'previous_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.ArticleRevision']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'revision_number': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'user_message': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'wiki.reusableplugin': {
            'Meta': {'object_name': 'ReusablePlugin', '_ormbases': ['wiki.ArticlePlugin']},
            'articleplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['wiki.ArticlePlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'articles': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'shared_plugins_set'", 'symmetrical': 'False', 'to': "orm['wiki.Article']"})
        }
    }

    complete_apps = ['template']
