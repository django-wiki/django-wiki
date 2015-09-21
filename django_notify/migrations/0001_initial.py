# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('url', models.URLField(null=True, verbose_name='link for notification', blank=True)),
                ('is_viewed', models.BooleanField(default=False)),
                ('is_emailed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'notify_notification',
                'verbose_name': 'notification',
                'verbose_name_plural': 'notifications',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NotificationType',
            fields=[
                ('key', models.CharField(max_length=128, unique=True, serialize=False, verbose_name='unique key', primary_key=True)),
                ('label', models.CharField(max_length=128, null=True, verbose_name='verbose name', blank=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'db_table': 'notify_notificationtype',
                'verbose_name': 'type',
                'verbose_name_plural': 'types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('interval', models.SmallIntegerField(default=0, verbose_name='interval', choices=[(0, 'instantly'), (23, 'daily'), (167, 'weekly')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'notify_settings',
                'verbose_name': 'settings',
                'verbose_name_plural': 'settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('subscription_id', models.AutoField(serialize=False, primary_key=True)),
                ('object_id', models.CharField(help_text='Leave this blank to subscribe to any kind of object', max_length=64, null=True, blank=True)),
                ('send_emails', models.BooleanField(default=True)),
                ('notification_type', models.ForeignKey(to='django_notify.NotificationType')),
                ('settings', models.ForeignKey(to='django_notify.Settings')),
            ],
            options={
                'db_table': 'notify_subscription',
                'verbose_name': 'subscription',
                'verbose_name_plural': 'subscriptions',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='notification',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='django_notify.Subscription', null=True),
            preserve_default=True,
        ),
    ]
