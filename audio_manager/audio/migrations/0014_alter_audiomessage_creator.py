# Generated by Django 4.2.1 on 2023-06-10 21:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("audio", "0013_alter_audiomessage_assigned_users_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="audiomessage",
            name="creator",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
