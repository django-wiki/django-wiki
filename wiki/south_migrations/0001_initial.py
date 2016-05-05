# -*- coding: utf-8 -*-
from django.db import models
from south.db import db
from south.utils import datetime_utils as datetime
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Article'
        db.create_table(u'wiki_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('current_revision', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name=u'current_set', unique=True, null=True, to=orm['wiki.ArticleRevision'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'owned_articles', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('group_read', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('group_write', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('other_read', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('other_write', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'wiki', ['Article'])

        # Adding model 'ArticleForObject'
        db.create_table(u'wiki_articleforobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.Article'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'content_type_set_for_articleforobject', to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_mptt', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'wiki', ['ArticleForObject'])

        # Adding unique constraint on 'ArticleForObject', fields ['content_type', 'object_id']
        db.create_unique(u'wiki_articleforobject', ['content_type_id', 'object_id'])

        # Adding model 'ArticleRevision'
        db.create_table(u'wiki_articlerevision', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('revision_number', self.gf('django.db.models.fields.IntegerField')()),
            ('user_message', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('automatic_log', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('previous_revision', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.ArticleRevision'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.Article'])),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal(u'wiki', ['ArticleRevision'])

        # Adding unique constraint on 'ArticleRevision', fields ['article', 'revision_number']
        db.create_unique(u'wiki_articlerevision', ['article_id', 'revision_number'])

        # Adding model 'URLPath'
        db.create_table(u'wiki_urlpath', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.Article'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name=u'children', null=True, to=orm['wiki.URLPath'])),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'wiki', ['URLPath'])

        # Adding unique constraint on 'URLPath', fields ['site', 'parent', 'slug']
        db.create_unique(u'wiki_urlpath', ['site_id', 'parent_id', 'slug'])

        # Adding model 'ArticlePlugin'
        db.create_table(u'wiki_articleplugin', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.Article'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'wiki', ['ArticlePlugin'])

        # Adding model 'ReusablePlugin'
        db.create_table(u'wiki_reusableplugin', (
            (u'articleplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wiki.ArticlePlugin'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'wiki', ['ReusablePlugin'])

        # Adding M2M table for field articles on 'ReusablePlugin'
        m2m_table_name = db.shorten_name(u'wiki_reusableplugin_articles')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reusableplugin', models.ForeignKey(orm[u'wiki.reusableplugin'], null=False)),
            ('article', models.ForeignKey(orm[u'wiki.article'], null=False))
        ))
        db.create_unique(m2m_table_name, ['reusableplugin_id', 'article_id'])

        # Adding model 'SimplePlugin'
        db.create_table(u'wiki_simpleplugin', (
            (u'articleplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wiki.ArticlePlugin'], unique=True, primary_key=True)),
            ('article_revision', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.ArticleRevision'])),
        ))
        db.send_create_signal(u'wiki', ['SimplePlugin'])

        # Adding model 'RevisionPlugin'
        db.create_table(u'wiki_revisionplugin', (
            (u'articleplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wiki.ArticlePlugin'], unique=True, primary_key=True)),
            ('current_revision', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name=u'plugin_set', unique=True, null=True, to=orm['wiki.RevisionPluginRevision'])),
        ))
        db.send_create_signal(u'wiki', ['RevisionPlugin'])

        # Adding model 'RevisionPluginRevision'
        db.create_table(u'wiki_revisionpluginrevision', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('revision_number', self.gf('django.db.models.fields.IntegerField')()),
            ('user_message', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('automatic_log', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('previous_revision', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.RevisionPluginRevision'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('plugin', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'revision_set', to=orm['wiki.RevisionPlugin'])),
        ))
        db.send_create_signal(u'wiki', ['RevisionPluginRevision'])


    def backwards(self, orm):
        # Removing unique constraint on 'URLPath', fields ['site', 'parent', 'slug']
        db.delete_unique(u'wiki_urlpath', ['site_id', 'parent_id', 'slug'])

        # Removing unique constraint on 'ArticleRevision', fields ['article', 'revision_number']
        db.delete_unique(u'wiki_articlerevision', ['article_id', 'revision_number'])

        # Removing unique constraint on 'ArticleForObject', fields ['content_type', 'object_id']
        db.delete_unique(u'wiki_articleforobject', ['content_type_id', 'object_id'])

        # Deleting model 'Article'
        db.delete_table(u'wiki_article')

        # Deleting model 'ArticleForObject'
        db.delete_table(u'wiki_articleforobject')

        # Deleting model 'ArticleRevision'
        db.delete_table(u'wiki_articlerevision')

        # Deleting model 'URLPath'
        db.delete_table(u'wiki_urlpath')

        # Deleting model 'ArticlePlugin'
        db.delete_table(u'wiki_articleplugin')

        # Deleting model 'ReusablePlugin'
        db.delete_table(u'wiki_reusableplugin')

        # Removing M2M table for field articles on 'ReusablePlugin'
        db.delete_table(db.shorten_name(u'wiki_reusableplugin_articles'))

        # Deleting model 'SimplePlugin'
        db.delete_table(u'wiki_simpleplugin')

        # Deleting model 'RevisionPlugin'
        db.delete_table(u'wiki_revisionplugin')

        # Deleting model 'RevisionPluginRevision'
        db.delete_table(u'wiki_revisionpluginrevision')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'wiki.article': {
            'Meta': {'object_name': 'Article'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_revision': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "u'current_set'", 'unique': 'True', 'null': 'True', 'to': u"orm['wiki.ArticleRevision']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'group_read': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'group_write': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'other_read': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'other_write': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'owned_articles'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"})
        },
        u'wiki.articleforobject': {
            'Meta': {'unique_together': "((u'content_type', u'object_id'),)", 'object_name': 'ArticleForObject'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wiki.Article']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'content_type_set_for_articleforobject'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_mptt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'wiki.articleplugin': {
            'Meta': {'object_name': 'ArticlePlugin'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wiki.Article']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'wiki.articlerevision': {
            'Meta': {'ordering': "(u'created',)", 'unique_together': "((u'article', u'revision_number'),)", 'object_name': 'ArticleRevision'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wiki.Article']"}),
            'automatic_log': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'previous_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wiki.ArticleRevision']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'revision_number': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'user_message': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'wiki.reusableplugin': {
            'Meta': {'object_name': 'ReusablePlugin', '_ormbases': [u'wiki.ArticlePlugin']},
            u'articleplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wiki.ArticlePlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'articles': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'shared_plugins_set'", 'symmetrical': 'False', 'to': u"orm['wiki.Article']"})
        },
        u'wiki.revisionplugin': {
            'Meta': {'object_name': 'RevisionPlugin', '_ormbases': [u'wiki.ArticlePlugin']},
            u'articleplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wiki.ArticlePlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'current_revision': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "u'plugin_set'", 'unique': 'True', 'null': 'True', 'to': u"orm['wiki.RevisionPluginRevision']"})
        },
        u'wiki.revisionpluginrevision': {
            'Meta': {'ordering': "(u'-created',)", 'object_name': 'RevisionPluginRevision'},
            'automatic_log': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'plugin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'revision_set'", 'to': u"orm['wiki.RevisionPlugin']"}),
            'previous_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wiki.RevisionPluginRevision']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'revision_number': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'user_message': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'wiki.simpleplugin': {
            'Meta': {'object_name': 'SimplePlugin', '_ormbases': [u'wiki.ArticlePlugin']},
            'article_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wiki.ArticleRevision']"}),
            u'articleplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wiki.ArticlePlugin']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'wiki.urlpath': {
            'Meta': {'unique_together': "((u'site', u'parent', u'slug'),)", 'object_name': 'URLPath'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wiki.Article']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "u'children'", 'null': 'True', 'to': u"orm['wiki.URLPath']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['wiki']
