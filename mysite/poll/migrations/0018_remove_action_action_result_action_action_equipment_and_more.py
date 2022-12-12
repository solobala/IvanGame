# Generated by Django 4.1.3 on 2022-12-11 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0017_action"),
    ]

    operations = [
        migrations.RemoveField(model_name="action", name="action_result",),
        migrations.AddField(
            model_name="action",
            name="action_equipment",
            field=models.JSONField(blank=True, null=True, verbose_name="Снаряжение"),
        ),
        migrations.AddField(
            model_name="action",
            name="action_permissions",
            field=models.JSONField(blank=True, null=True, verbose_name="Умения"),
        ),
        migrations.AddField(
            model_name="action",
            name="action_points",
            field=models.JSONField(
                blank=True, null=True, verbose_name="Характеристики"
            ),
        ),
        migrations.AddField(
            model_name="action",
            name="action_resistanses",
            field=models.JSONField(
                blank=True, null=True, verbose_name="Сопротивляемость"
            ),
        ),
    ]
