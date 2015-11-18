# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_notify', '0001_initial'),
        ('wiki', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlesubscription',
            name='articleplugin_ptr',
        ),
        migrations.RemoveField(
            model_name='articlesubscription',
            name='subscription_ptr',
        ),
        migrations.DeleteModel(
            name='ArticleSubscription',
        ),
    ]
