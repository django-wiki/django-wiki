# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('wiki_attachments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='attachment',
            table='wiki_attachments_attachment',
        ),
        migrations.AlterModelTable(
            name='attachmentrevision',
            table='wiki_attachments_attachmentrevision',
        ),
    ]
