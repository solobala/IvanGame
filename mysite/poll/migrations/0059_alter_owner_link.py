# Generated by Django 4.1.3 on 2023-01-02 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0058_alter_region_location"),
    ]

    operations = [
        migrations.AlterField(
            model_name="owner",
            name="link",
            field=models.URLField(
                blank=True, max_length=9, null=True, verbose_name="Ссылка"
            ),
        ),
    ]