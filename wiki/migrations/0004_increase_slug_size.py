# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0003_ip_address_conv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlpath',
            name='slug',
            field=models.SlugField(max_length=255, null=True, verbose_name='slug', blank=True),
        ),
    ]
