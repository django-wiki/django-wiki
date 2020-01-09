from django.db import migrations, models


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ("wiki_notifications", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="articlesubscription", table="wiki_notifications_articlesubscription",
        ),
    ]
