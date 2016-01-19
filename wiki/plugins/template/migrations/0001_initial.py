# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wiki', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('template_title', models.SlugField(unique=True)),
                ('extend_to_children', models.BooleanField(
                    default=False, verbose_name='extend')),
            ],
            options={
                'verbose_name_plural': 'templates',
                'verbose_name': 'template',
            },
            bases=('wiki.reusableplugin',),
        ),
        migrations.CreateModel(
            name='TemplateRevision',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('revision_number', models.IntegerField(
                    verbose_name='revision number', editable=False)),
                ('user_message', models.TextField(blank=True)),
                ('automatic_log', models.TextField(blank=True, editable=False)),
                ('ip_address', models.IPAddressField(
                    verbose_name='IP address', null=True, blank=True, editable=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='user',
                 null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, to_field='id')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.BooleanField(
                    default=False, verbose_name='deleted')),
                ('locked', models.BooleanField(
                    default=False, verbose_name='locked')),
                ('template', models.ForeignKey(
                    to='template.Template', to_field='reusableplugin_ptr')),
                ('template_content', models.TextField(verbose_name='template content',
                 help_text='Does not support nested template.', blank=True)),
                ('description', models.TextField(
                    verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name_plural': 'template revisions',
                'ordering': ('created',),
                'verbose_name': 'template revision',
                'get_latest_by': 'revision_number',
            },
            bases=(models.Model,),
        ),
    ]
