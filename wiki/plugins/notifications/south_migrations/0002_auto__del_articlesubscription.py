# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ArticleSubscription'
        db.delete_table('notifications_articlesubscription')


    def backwards(self, orm):
        # Adding model 'ArticleSubscription'
        db.create_table('notifications_articlesubscription', (
            ('articleplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wiki.ArticlePlugin'], unique=True, primary_key=True)),
            ('subscription_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['django_notify.Subscription'], unique=True)),
        ))
        db.send_create_signal('notifications', ['ArticleSubscription'])


    models = {
        
    }

    complete_apps = ['notifications']