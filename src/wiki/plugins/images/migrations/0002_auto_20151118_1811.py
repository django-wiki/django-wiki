# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('wiki_images', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='image',
            table='wiki_images_image',
        ),
        migrations.AlterModelTable(
            name='imagerevision',
            table='wiki_images_imagerevision',
        ),
    ]
