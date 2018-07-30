import django.db.models.deletion
import wiki.plugins.attachments.models
from django.conf import settings
from django.db import migrations, models
from django.db.models.fields import GenericIPAddressField as IPAddressField


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('reusableplugin_ptr', models.OneToOneField(parent_link=True, serialize=False, primary_key=True, to='wiki.ReusablePlugin', auto_created=True, on_delete=models.CASCADE)),
                ('original_filename', models.CharField(max_length=256, verbose_name='original filename', blank=True, null=True)),
            ],
            options={
                'verbose_name': 'attachment',
                'verbose_name_plural': 'attachments',
            },
            bases=('wiki.reusableplugin',),
        ),
        migrations.CreateModel(
            name='AttachmentRevision',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('revision_number', models.IntegerField(verbose_name='revision number', editable=False)),
                ('user_message', models.TextField(blank=True)),
                ('automatic_log', models.TextField(editable=False, blank=True)),
                ('ip_address', IPAddressField(editable=False, verbose_name='IP address', blank=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
                ('locked', models.BooleanField(default=False, verbose_name='locked')),
                ('file', models.FileField(max_length=255, verbose_name='file', upload_to=wiki.plugins.attachments.models.upload_path)),
                ('description', models.TextField(blank=True)),
                ('attachment', models.ForeignKey(to='wiki_attachments.Attachment', on_delete=models.CASCADE)),
                ('previous_revision', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, to='wiki_attachments.AttachmentRevision', null=True)),
                ('user', models.ForeignKey(blank=True, verbose_name='user', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('created',),
                'get_latest_by': 'revision_number',
                'verbose_name': 'attachment revision',
                'verbose_name_plural': 'attachment revisions',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='attachment',
            name='current_revision',
            field=models.OneToOneField(to='wiki_attachments.AttachmentRevision', blank=True, verbose_name='current revision', related_name='current_set', help_text='The revision of this attachment currently in use (on all articles using the attachment)', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
