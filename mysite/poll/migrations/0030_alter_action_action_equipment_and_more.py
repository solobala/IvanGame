# Generated by Django 4.1.3 on 2022-12-12 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0029_alter_action_action_points"),
    ]

    operations = [
        migrations.AlterField(
            model_name="action",
            name="action_equipment",
            field=models.JSONField(
                blank=True, default=dict, null=True, verbose_name="Снаряжение"
            ),
        ),
        migrations.AlterField(
            model_name="action",
            name="action_permissions",
            field=models.JSONField(
                blank=True, default=dict, null=True, verbose_name="Умения"
            ),
        ),
        migrations.AlterField(
            model_name="action",
            name="action_points",
            field=models.JSONField(
                blank=True, default=dict, null=True, verbose_name="Характеристики"
            ),
        ),
        migrations.AlterField(
            model_name="action",
            name="action_resistances",
            field=models.JSONField(
                blank=True, default=dict, null=True, verbose_name="Сопротивляемость"
            ),
        ),
    ]
