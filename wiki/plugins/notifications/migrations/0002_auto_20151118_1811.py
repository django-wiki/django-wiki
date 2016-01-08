# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki_notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='articlesubscription',
            table='wiki_notifications_articlesubscription',
        ),
    ]
