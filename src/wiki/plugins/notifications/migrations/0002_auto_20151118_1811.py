from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ("wiki_notifications", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="articlesubscription",
            table="wiki_notifications_articlesubscription",
        ),
    ]
