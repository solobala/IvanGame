# Generated by Django 4.1.3 on 2022-12-27 06:37

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0055_action_level_feature_level_personbar_fov_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Consumable",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "consumable_name",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                (
                    "consumable_description",
                    ckeditor.fields.RichTextField(
                        blank=True, null=True, verbose_name="Описание"
                    ),
                ),
                (
                    "points_to_make",
                    models.JSONField(
                        blank=True,
                        null=True,
                        verbose_name="очки характеристик для создания",
                    ),
                ),
                (
                    "points_from_use",
                    models.JSONField(
                        blank=True,
                        null=True,
                        verbose_name="очки характеристик от применения",
                    ),
                ),
                (
                    "resistances_from_use",
                    models.JSONField(
                        blank=True,
                        null=True,
                        verbose_name="очки сопротивлений от применения",
                    ),
                ),
                (
                    "conditions",
                    models.JSONField(
                        blank=True, null=True, verbose_name="очки кондиций"
                    ),
                ),
                (
                    "damage_from_use",
                    models.JSONField(
                        blank=True,
                        null=True,
                        verbose_name="очки урона противнику от применения",
                    ),
                ),
                (
                    "sale_price",
                    models.IntegerField(default=100, verbose_name="Цена продажи"),
                ),
                (
                    "buy_price",
                    models.IntegerField(default=100, verbose_name="Цена покупки"),
                ),
            ],
            options={
                "verbose_name": "Consumable",
                "verbose_name_plural": "Consumable",
                "db_table": "consumable",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="Thing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("thing_name", models.CharField(blank=True, max_length=128, null=True)),
                (
                    "thing_description",
                    ckeditor.fields.RichTextField(
                        blank=True, null=True, verbose_name="Описание"
                    ),
                ),
                (
                    "points_to_make",
                    models.JSONField(
                        blank=True,
                        null=True,
                        verbose_name="очки характеристик для создания",
                    ),
                ),
                (
                    "points_to_use",
                    models.JSONField(
                        blank=True,
                        null=True,
                        verbose_name="очки характеристик для применения",
                    ),
                ),
                (
                    "equipment_to_use",
                    models.JSONField(
                        blank=True, null=True, verbose_name="слоты для применения"
                    ),
                ),
                (
                    "points_from_use",
                    models.JSONField(
                        blank=True,
                        null=True,
                        verbose_name="очки характеристик от применения",
                    ),
                ),
                (
                    "resistances_from_use",
                    models.JSONField(
                        blank=True,
                        null=True,
                        verbose_name="очки сопротивлений от применения",
                    ),
                ),
                (
                    "permissions_from_use",
                    models.JSONField(
                        blank=True, null=True, verbose_name="очки навыков от применения"
                    ),
                ),
                (
                    "equipment_from_use",
                    models.JSONField(
                        blank=True,
                        null=True,
                        verbose_name="расширение слотов от применения",
                    ),
                ),
                (
                    "conditions",
                    models.JSONField(
                        blank=True, null=True, verbose_name="очки кондиций"
                    ),
                ),
                (
                    "damage_from_use",
                    models.JSONField(
                        blank=True,
                        null=True,
                        verbose_name="очки урона противнику от применения",
                    ),
                ),
                (
                    "sale_price",
                    models.IntegerField(default=100, verbose_name="Цена продажи"),
                ),
                (
                    "buy_price",
                    models.IntegerField(default=100, verbose_name="Цена покупки"),
                ),
            ],
            options={
                "verbose_name": "Thing",
                "verbose_name_plural": "Things",
                "db_table": "thing",
                "managed": True,
            },
        ),
        migrations.AddField(
            model_name="person",
            name="features",
            field=models.ManyToManyField(blank=True, null=True, to="poll.feature"),
        ),
    ]
