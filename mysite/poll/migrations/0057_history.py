# Generated by Django 4.1.3 on 2022-12-28 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0056_consumable_thing_person_features"),
    ]

    operations = [
        migrations.CreateModel(
            name="History",
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
                    "move_number_begin",
                    models.IntegerField(
                        verbose_name="Номер хода - начало действия Персонажа"
                    ),
                ),
                (
                    "move_number_end",
                    models.IntegerField(
                        verbose_name="Номер хода - конец действия Персонажа"
                    ),
                ),
                (
                    "points_old",
                    models.JSONField(
                        blank=True, null=True, verbose_name="Прежние очки характеристик"
                    ),
                ),
                (
                    "points_new",
                    models.JSONField(
                        blank=True, null=True, verbose_name="Новые очки характеристик"
                    ),
                ),
                (
                    "permissions_old",
                    models.JSONField(
                        blank=True, null=True, verbose_name="Прежние навыки"
                    ),
                ),
                (
                    "permissions_new",
                    models.JSONField(
                        blank=True, null=True, verbose_name="Новые навыки"
                    ),
                ),
                (
                    "resistances_old",
                    models.JSONField(
                        blank=True, null=True, verbose_name="Прежние сопротивления"
                    ),
                ),
                (
                    "resistances_new",
                    models.JSONField(
                        blank=True, null=True, verbose_name="Новые сопротивления"
                    ),
                ),
                (
                    "equipment_old",
                    models.JSONField(
                        blank=True, null=True, verbose_name="Прежнее снаряжение"
                    ),
                ),
                (
                    "equipment_new",
                    models.JSONField(
                        blank=True, null=True, verbose_name="Новое снаряжение"
                    ),
                ),
                (
                    "un_points_old",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Прежние нераспределенные очки",
                    ),
                ),
                (
                    "un_points_new",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Новые нераспределенные очки",
                    ),
                ),
                (
                    "un_permissions_old",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Прежние нераспределенные навыки",
                    ),
                ),
                (
                    "un_permissions_new",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Новые нераспределенные навыки",
                    ),
                ),
                (
                    "fov_old",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Прежняя область обзора"
                    ),
                ),
                (
                    "fov_new",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Новая область обзора"
                    ),
                ),
                (
                    "rov_old",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Прежняя дальность обзора"
                    ),
                ),
                (
                    "rov_new",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Новая дальность обзора"
                    ),
                ),
                (
                    "level_old",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Прежний уровень"
                    ),
                ),
                (
                    "level_new",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Новый уровень"
                    ),
                ),
                ("last_update", models.TimeField(auto_now=True)),
                (
                    "action",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="poll.action",
                    ),
                ),
                (
                    "action_type",
                    models.ManyToManyField(
                        blank=True,
                        null=True,
                        to="poll.actiontype",
                        verbose_name="тип действия Персонажа",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="poll.person",
                    ),
                ),
            ],
            options={
                "verbose_name": "History",
                "db_table": "history",
                "managed": True,
            },
        ),
    ]
