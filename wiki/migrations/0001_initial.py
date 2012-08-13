# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Article'
        db.create_table('wiki_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('current_revision', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='current_set', unique=True, null=True, to=orm['wiki.ArticleRevision'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'], null=True, blank=True)),
            ('group_read', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('group_write', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('other_read', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('other_write', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('wiki', ['Article'])

        # Adding model 'ArticleForObject'
        db.create_table('wiki_articleforobject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.Article'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='content_type_set_for_articleforobject', to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_mptt', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('wiki', ['ArticleForObject'])

        # Adding unique constraint on 'ArticleForObject', fields ['content_type', 'object_id']
        db.create_unique('wiki_articleforobject', ['content_type_id', 'object_id'])

        # Adding model 'ArticleRevision'
        db.create_table('wiki_articlerevision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('revision_number', self.gf('django.db.models.fields.IntegerField')()),
            ('user_message', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('automatic_log', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('previous_revision', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.ArticleRevision'], null=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.Article'])),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('redirect', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='redirect_set', null=True, to=orm['wiki.Article'])),
        ))
        db.send_create_signal('wiki', ['ArticleRevision'])

        # Adding unique constraint on 'ArticleRevision', fields ['article', 'revision_number']
        db.create_unique('wiki_articlerevision', ['article_id', 'revision_number'])

        # Adding model 'URLPath'
        db.create_table('wiki_urlpath', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['wiki.URLPath'])),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('wiki', ['URLPath'])

        # Adding unique constraint on 'URLPath', fields ['site', 'parent', 'slug']
        db.create_unique('wiki_urlpath', ['site_id', 'parent_id', 'slug'])

        # Adding model 'ArticlePlugin'
        db.create_table('wiki_articleplugin', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.Article'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('wiki', ['ArticlePlugin'])

        # Adding model 'ReusablePlugin'
        db.create_table('wiki_reusableplugin', (
            ('articleplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wiki.ArticlePlugin'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('wiki', ['ReusablePlugin'])

        # Adding M2M table for field articles on 'ReusablePlugin'
        db.create_table('wiki_reusableplugin_articles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reusableplugin', models.ForeignKey(orm['wiki.reusableplugin'], null=False)),
            ('article', models.ForeignKey(orm['wiki.article'], null=False))
        ))
        db.create_unique('wiki_reusableplugin_articles', ['reusableplugin_id', 'article_id'])

        # Adding model 'RevisionPlugin'
        db.create_table('wiki_revisionplugin', (
            ('articleplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wiki.ArticlePlugin'], unique=True, primary_key=True)),
            ('revision', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.ArticleRevision'])),
        ))
        db.send_create_signal('wiki', ['RevisionPlugin'])


    def backwards(self, orm):
        # Removing unique constraint on 'URLPath', fields ['site', 'parent', 'slug']
        db.delete_unique('wiki_urlpath', ['site_id', 'parent_id', 'slug'])

        # Removing unique constraint on 'ArticleRevision', fields ['article', 'revision_number']
        db.delete_unique('wiki_articlerevision', ['article_id', 'revision_number'])

        # Removing unique constraint on 'ArticleForObject', fields ['content_type', 'object_id']
        db.delete_unique('wiki_articleforobject', ['content_type_id', 'object_id'])

        # Deleting model 'Article'
        db.delete_table('wiki_article')

        # Deleting model 'ArticleForObject'
        db.delete_table('wiki_articleforobject')

        # Deleting model 'ArticleRevision'
        db.delete_table('wiki_articlerevision')

        # Deleting model 'URLPath'
        db.delete_table('wiki_urlpath')

        # Deleting model 'ArticlePlugin'
        db.delete_table('wiki_articleplugin')

        # Deleting model 'ReusablePlugin'
        db.delete_table('wiki_reusableplugin')

        # Removing M2M table for field articles on 'ReusablePlugin'
        db.delete_table('wiki_reusableplugin_articles')

        # Deleting model 'RevisionPlugin'
        db.delete_table('wiki_revisionplugin')


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
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            'group_read': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'group_write': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'other_read': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'other_write': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
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
            'redirect': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'redirect_set'", 'null': 'True', 'to': "orm['wiki.Article']"}),
            'revision_number': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'user_message': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'wiki.reusableplugin': {
            'Meta': {'object_name': 'ReusablePlugin', '_ormbases': ['wiki.ArticlePlugin']},
            'articleplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['wiki.ArticlePlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'articles': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'shared_plugins_set'", 'symmetrical': 'False', 'to': "orm['wiki.Article']"})
        },
        'wiki.revisionplugin': {
            'Meta': {'object_name': 'RevisionPlugin', '_ormbases': ['wiki.ArticlePlugin']},
            'articleplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['wiki.ArticlePlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'revision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.ArticleRevision']"})
        },
        'wiki.urlpath': {
            'Meta': {'unique_together': "(('site', 'parent', 'slug'),)", 'object_name': 'URLPath'},
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