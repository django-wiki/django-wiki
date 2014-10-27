# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('template', '0002_template_reusableplugin_ptr'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='current_revision',
            field=models.OneToOneField(to='template.TemplateRevision', verbose_name='current revision', to_field='id', blank=True, help_text='The revision of this template currently in use (on all articles using the template)', null=True),
            preserve_default=True,
        ),
    ]
