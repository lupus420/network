# Generated by Django 4.2.3 on 2023-09-13 09:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0007_remove_comment_likes_comment_likes"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="comments",
        ),
        migrations.AddField(
            model_name="comment",
            name="parent_post",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="network.post",
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="likes",
            field=models.ManyToManyField(
                blank=True, related_name="liked_comment", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
