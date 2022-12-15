# Generated by Django 4.1.3 on 2022-12-12 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0027_alter_action_sp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="action",
            name="points",
            field=models.JSONField(
                default={
                    "AP": 0,
                    "BP": 0,
                    "CP": 0,
                    "FP": 0,
                    "IP": 0,
                    "LP": 0,
                    "MP": 0,
                    "PP": 0,
                    "SP": 0,
                },
                verbose_name="Характеристики",
            ),
        ),
    ]
