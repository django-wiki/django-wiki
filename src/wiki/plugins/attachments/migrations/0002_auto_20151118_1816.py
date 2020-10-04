from django.db import migrations
from django.db import models


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
