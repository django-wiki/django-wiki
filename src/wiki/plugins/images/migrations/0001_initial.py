import wiki.plugins.images.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('revisionplugin_ptr', models.OneToOneField(to='wiki.RevisionPlugin', primary_key=True, auto_created=True, parent_link=True, serialize=False, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
            bases=('wiki.revisionplugin',),
        ),
        migrations.CreateModel(
            name='ImageRevision',
            fields=[
                ('revisionpluginrevision_ptr', models.OneToOneField(to='wiki.RevisionPluginRevision', primary_key=True, auto_created=True, parent_link=True, serialize=False, on_delete=models.CASCADE)),
                ('image', models.ImageField(null=True, blank=True, height_field='height', max_length=2000, width_field='width', upload_to=wiki.plugins.images.models.upload_path)),
                ('width', models.SmallIntegerField(null=True, blank=True)),
                ('height', models.SmallIntegerField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'image revision',
                'verbose_name_plural': 'image revisions',
                'ordering': ('-created',),
            },
            bases=('wiki.revisionpluginrevision',),
        ),
    ]
