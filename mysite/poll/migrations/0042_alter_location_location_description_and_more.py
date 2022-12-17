# Generated by Django 4.1.3 on 2022-12-17 17:45

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0041_alter_location_zone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="location_description",
            field=ckeditor.fields.RichTextField(
                blank=True, null=True, verbose_name="Описание"
            ),
        ),
        migrations.AlterField(
            model_name="owner",
            name="owner_img",
            field=models.ImageField(
                upload_to="media/euploads", verbose_name="Изображение"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="biography",
            field=ckeditor.fields.RichTextField(
                blank=True, null=True, verbose_name="Биография"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="birth_date",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Дата рождения"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="character",
            field=ckeditor.fields.RichTextField(
                blank=True, null=True, verbose_name="Характер"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="death_date",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Дата гибели"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="interests",
            field=ckeditor.fields.RichTextField(
                blank=True, null=True, verbose_name="Интересы"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="link",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Ссылка"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="location_birth",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Место возрождения"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="location_death",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Место гибели"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="person_img",
            field=models.ImageField(
                default="media/euploads/python.png",
                upload_to="",
                verbose_name="Изображение",
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="person_name",
            field=models.CharField(
                blank=True, max_length=45, null=True, verbose_name="Персонаж"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="phobias",
            field=ckeditor.fields.RichTextField(
                blank=True, null=True, verbose_name="Фобии"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="race",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="poll.race",
                verbose_name="Раса",
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="status",
            field=models.IntegerField(
                choices=[(0, "Freezed"), (1, "Free"), (2, "Busy")],
                default=1,
                verbose_name="Статус",
            ),
        ),
    ]