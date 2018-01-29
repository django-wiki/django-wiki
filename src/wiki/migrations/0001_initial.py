# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import mptt.fields
from django.conf import settings
from django.db import migrations, models
from django.db.models.fields import GenericIPAddressField as IPAddressField

from wiki.conf.settings import GROUP_MODEL


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(verbose_name='created', auto_now_add=True)),
                ('modified', models.DateTimeField(verbose_name='modified', auto_now=True, help_text='Article properties last modified')),
                ('group_read', models.BooleanField(default=True, verbose_name='group read access')),
                ('group_write', models.BooleanField(default=True, verbose_name='group write access')),
                ('other_read', models.BooleanField(default=True, verbose_name='others read access')),
                ('other_write', models.BooleanField(default=True, verbose_name='others write access')),
            ],
            options={
                'permissions': (('moderate', 'Can edit all articles and lock/unlock/restore'), ('assign', 'Can change ownership of any article'), ('grant', 'Can assign permissions to other users')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleForObject',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(verbose_name='object ID')),
                ('is_mptt', models.BooleanField(default=False, editable=False)),
                ('article', models.ForeignKey(to='wiki.Article', on_delete=models.CASCADE)),
                ('content_type', models.ForeignKey(related_name='content_type_set_for_articleforobject', verbose_name='content type', to='contenttypes.ContentType', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name_plural': 'Articles for object',
                'verbose_name': 'Article for object',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticlePlugin',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleRevision',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('revision_number', models.IntegerField(verbose_name='revision number', editable=False)),
                ('user_message', models.TextField(blank=True)),
                ('automatic_log', models.TextField(blank=True, editable=False)),
                ('ip_address', IPAddressField(null=True, verbose_name='IP address', blank=True, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
                ('locked', models.BooleanField(default=False, verbose_name='locked')),
                ('content', models.TextField(blank=True, verbose_name='article contents')),
                ('title', models.CharField(max_length=512, verbose_name='article title', help_text='Each revision contains a title field that must be filled out, even if the title has not changed')),
                ('article', models.ForeignKey(to='wiki.Article', verbose_name='article', on_delete=models.CASCADE)),
                ('previous_revision', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wiki.ArticleRevision')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'get_latest_by': 'revision_number',
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReusablePlugin',
            fields=[
                ('articleplugin_ptr', models.OneToOneField(primary_key=True, parent_link=True, to='wiki.ArticlePlugin', serialize=False, auto_created=True, on_delete=models.CASCADE)),
                ('articles', models.ManyToManyField(related_name='shared_plugins_set', to='wiki.Article')),
            ],
            options={
            },
            bases=('wiki.articleplugin',),
        ),
        migrations.CreateModel(
            name='RevisionPlugin',
            fields=[
                ('articleplugin_ptr', models.OneToOneField(primary_key=True, parent_link=True, to='wiki.ArticlePlugin', serialize=False, auto_created=True, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=('wiki.articleplugin',),
        ),
        migrations.CreateModel(
            name='RevisionPluginRevision',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('revision_number', models.IntegerField(verbose_name='revision number', editable=False)),
                ('user_message', models.TextField(blank=True)),
                ('automatic_log', models.TextField(blank=True, editable=False)),
                ('ip_address', IPAddressField(null=True, verbose_name='IP address', blank=True, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
                ('locked', models.BooleanField(default=False, verbose_name='locked')),
                ('plugin', models.ForeignKey(related_name='revision_set', to='wiki.RevisionPlugin', on_delete=models.CASCADE)),
                ('previous_revision', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wiki.RevisionPluginRevision')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'get_latest_by': 'revision_number',
                'ordering': ('-created',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SimplePlugin',
            fields=[
                ('articleplugin_ptr', models.OneToOneField(primary_key=True, parent_link=True, to='wiki.ArticlePlugin', serialize=False, auto_created=True, on_delete=models.CASCADE)),
                ('article_revision', models.ForeignKey(to='wiki.ArticleRevision', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=('wiki.articleplugin',),
        ),
        migrations.CreateModel(
            name='URLPath',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('slug', models.SlugField(null=True, blank=True, verbose_name='slug')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('article', models.ForeignKey(help_text='This field is automatically updated, but you need to populate it when creating a new URL path.', on_delete=django.db.models.deletion.CASCADE, to='wiki.Article', verbose_name='article')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, help_text='Position of URL path in the tree.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='wiki.URLPath')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
            options={
                'verbose_name_plural': 'URL paths',
                'verbose_name': 'URL path',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='urlpath',
            unique_together=set([('site', 'parent', 'slug')]),
        ),
        migrations.AddField(
            model_name='revisionplugin',
            name='current_revision',
            field=models.OneToOneField(related_name='plugin_set', null=True, help_text='The revision being displayed for this plugin. If you need to do a roll-back, simply change the value of this field.', blank=True, to='wiki.RevisionPluginRevision', verbose_name='current revision', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='articlerevision',
            unique_together=set([('article', 'revision_number')]),
        ),
        migrations.AddField(
            model_name='articleplugin',
            name='article',
            field=models.ForeignKey(to='wiki.Article', verbose_name='article', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='articleforobject',
            unique_together=set([('content_type', 'object_id')]),
        ),
        migrations.AddField(
            model_name='article',
            name='current_revision',
            field=models.OneToOneField(related_name='current_set', null=True, help_text='The revision being displayed for this article. If you need to do a roll-back, simply change the value of this field.', blank=True, to='wiki.ArticleRevision', verbose_name='current revision', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, help_text='Like in a UNIX file system, permissions can be given to a user according to group membership. Groups are handled through the Django auth system.', blank=True, to=GROUP_MODEL, verbose_name='group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='owner',
            field=models.ForeignKey(related_name='owned_articles', null=True, on_delete=django.db.models.deletion.SET_NULL, help_text='The owner of the article, usually the creator. The owner always has both read and write access.', blank=True, to=settings.AUTH_USER_MODEL, verbose_name='owner'),
            preserve_default=True,
        ),
    ]
