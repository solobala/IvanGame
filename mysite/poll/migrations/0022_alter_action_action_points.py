# Generated by Django 4.1.3 on 2022-12-12 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0021_alter_action_action_points"),
    ]

    operations = [
        migrations.AlterField(
            model_name="action",
            name="points",
            field=models.JSONField(default=dict, verbose_name="Характеристики"),
        ),
    ]
