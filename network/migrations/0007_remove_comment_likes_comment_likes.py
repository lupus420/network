# Generated by Django 4.2.3 on 2023-09-11 18:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0006_alter_follow_options_alter_follow_followed_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="likes",
        ),
        migrations.AddField(
            model_name="comment",
            name="likes",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="liked_comment",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
