# Generated by Django 4.1.3 on 2023-01-11 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0070_alter_person_location_birth"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="location_birth",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="location_birth",
                to="poll.location",
                verbose_name="Место возрождения",
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="location_death",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="location_death",
                to="poll.location",
                verbose_name="Место гибели",
            ),
        ),
    ]