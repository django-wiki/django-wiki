# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('template', '0003_template_current_revision'),
    ]

    operations = [
        migrations.AddField(
            model_name='templaterevision',
            name='previous_revision',
            field=models.ForeignKey(to='template.TemplateRevision', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, to_field='id'),
            preserve_default=True,
        ),
    ]
