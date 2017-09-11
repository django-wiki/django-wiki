# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wiki.plugins.images.models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0004_increase_slug_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('revisionplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wiki.RevisionPlugin')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
                'db_table': 'wiki_images_image',
            },
            bases=('wiki.revisionplugin',),
        ),
        migrations.CreateModel(
            name='ImageRevision',
            fields=[
                ('revisionpluginrevision_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wiki.RevisionPluginRevision')),
                ('image', models.ImageField(upload_to=wiki.plugins.images.models.upload_path, width_field=b'width', height_field=b'height', max_length=2000, blank=True, null=True)),
                ('width', models.SmallIntegerField(null=True, blank=True)),
                ('height', models.SmallIntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'image revision',
                'verbose_name_plural': 'image revisions',
                'db_table': 'wiki_images_imagerevision',
            },
            bases=('wiki.revisionpluginrevision',),
        ),
    ]
