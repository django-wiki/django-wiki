from django.db import migrations


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ("wiki_attachments", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="attachment",
            table="wiki_attachments_attachment",
        ),
        migrations.AlterModelTable(
            name="attachmentrevision",
            table="wiki_attachments_attachmentrevision",
        ),
    ]
