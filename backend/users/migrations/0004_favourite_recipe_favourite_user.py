# Generated by Django 5.2.1 on 2025-05-14 23:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0006_recipeingredient_amount"),
        ("users", "0003_user_avatar_user_is_subscribed_alter_user_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="favourite",
            name="recipe",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="in_favourites",
                to="recipes.recipe",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="favourite",
            name="user",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="favourites",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
