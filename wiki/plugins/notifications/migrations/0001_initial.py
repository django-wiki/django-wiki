# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0004_increase_slug_size'),
        ('django_notify', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleSubscription',
            fields=[
                ('subscription_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='django_notify.Subscription')),
                ('articleplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wiki.ArticlePlugin')),
            ],
            options={
                'db_table': 'wiki_notifications_articlesubscription',
            },
            bases=('wiki.articleplugin', 'django_notify.subscription'),
        ),
    ]
