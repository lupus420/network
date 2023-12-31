# Generated by Django 4.2.3 on 2023-09-09 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0004_remove_user_following"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="follow",
            constraint=models.UniqueConstraint(
                fields=("follower", "followed"), name="unique_follow"
            ),
        ),
    ]
