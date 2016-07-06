# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0002_remove_article_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlerevision',
            name='ip_address',
            field=models.GenericIPAddressField(verbose_name='IP address', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='attachmentrevision',
            name='ip_address',
            field=models.GenericIPAddressField(verbose_name='IP address', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='revisionpluginrevision',
            name='ip_address',
            field=models.GenericIPAddressField(verbose_name='IP address', null=True, editable=False, blank=True),
        ),
    ]
