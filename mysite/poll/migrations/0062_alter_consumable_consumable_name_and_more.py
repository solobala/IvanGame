# Generated by Django 4.1.3 on 2023-01-05 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0061_safe_inventory"),
    ]

    operations = [
        migrations.AlterField(
            model_name="consumable",
            name="consumable_name",
            field=models.CharField(
                blank=True, max_length=128, null=True, verbose_name="Название"
            ),
        ),
        migrations.AlterField(
            model_name="inventory",
            name="consumables_sum_value",
            field=models.IntegerField(
                default=0, verbose_name="Суммарный вес расходников"
            ),
        ),
        migrations.AlterField(
            model_name="inventory",
            name="inventory_max_weight",
            field=models.IntegerField(default=0, verbose_name="Максимальный веч"),
        ),
        migrations.AlterField(
            model_name="inventory",
            name="inventory_name",
            field=models.CharField(
                blank=True, max_length=128, null=True, verbose_name="Название"
            ),
        ),
        migrations.AlterField(
            model_name="inventory",
            name="person",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="poll.person",
                verbose_name="Персонаж",
            ),
        ),
        migrations.AlterField(
            model_name="inventory",
            name="thing_sum_value",
            field=models.IntegerField(
                default=0, verbose_name="Суммарный вес артефактов"
            ),
        ),
        migrations.AlterField(
            model_name="safe",
            name="location",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="poll.location",
                verbose_name="Локация",
            ),
        ),
        migrations.AlterField(
            model_name="safe",
            name="person",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="poll.person",
                verbose_name="Персонаж",
            ),
        ),
        migrations.AlterField(
            model_name="safe",
            name="safe_name",
            field=models.CharField(
                blank=True, max_length=128, null=True, verbose_name="Название"
            ),
        ),
        migrations.AlterField(
            model_name="thing",
            name="thing_name",
            field=models.CharField(
                blank=True, max_length=128, null=True, verbose_name="Название"
            ),
        ),
    ]
