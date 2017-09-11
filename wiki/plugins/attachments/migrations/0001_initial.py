# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wiki.plugins.attachments.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0004_increase_slug_size'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachmentRevision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('revision_number', models.IntegerField(verbose_name='revision number', editable=False)),
                ('user_message', models.TextField(blank=True)),
                ('automatic_log', models.TextField(editable=False, blank=True)),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP address', null=True, editable=False, blank=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
                ('locked', models.BooleanField(default=False, verbose_name='locked')),
                ('file', models.FileField(upload_to=wiki.plugins.attachments.models.upload_path, verbose_name='file')),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('created',),
                'get_latest_by': 'revision_number',
                'verbose_name': 'attachment revision',
                'verbose_name_plural': 'attachment revisions',
                'db_table': 'wiki_attachments_attachmentrevision',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('reusableplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wiki.ReusablePlugin')),
                ('original_filename', models.CharField(max_length=256, null=True, verbose_name='original filename', blank=True)),
            ],
            options={
                'verbose_name': 'attachment',
                'verbose_name_plural': 'attachments',
                'db_table': 'wiki_attachments_attachment',
            },
            bases=('wiki.reusableplugin',),
        ),
        migrations.AddField(
            model_name='attachmentrevision',
            name='attachment',
            field=models.ForeignKey(to='wiki_attachments.Attachment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attachmentrevision',
            name='previous_revision',
            field=models.ForeignKey(blank=True, to='wiki_attachments.AttachmentRevision', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attachmentrevision',
            name='user',
            field=models.ForeignKey(verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attachment',
            name='current_revision',
            field=models.OneToOneField(related_name='current_set', null=True, to='wiki_attachments.AttachmentRevision', blank=True, help_text='The revision of this attachment currently in use (on all articles using the attachment)', verbose_name='current revision'),
            preserve_default=True,
        ),
    ]
