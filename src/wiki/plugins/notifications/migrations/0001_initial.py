# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_nyt', '0006_auto_20141229_1630'),
        ('wiki', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleSubscription',
            fields=[
                ('articleplugin_ptr', models.OneToOneField(auto_created=True, to='wiki.ArticlePlugin', primary_key=True, parent_link=True, serialize=False, on_delete=models.CASCADE)),
                ('subscription', models.OneToOneField(to='django_nyt.Subscription', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=('wiki.articleplugin',),
        ),
        migrations.AlterUniqueTogether(
            name='articlesubscription',
            unique_together=set([('subscription', 'articleplugin_ptr')]),
        ),
    ]
