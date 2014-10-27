# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('template', '0001_initial'),
        ('wiki', '__first__'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='reusableplugin_ptr',
            field=models.OneToOneField(auto_created=True, to='wiki.ReusablePlugin', serialize=False, to_field='articleplugin_ptr', primary_key=True),
            preserve_default=True,
        ),
    ]
