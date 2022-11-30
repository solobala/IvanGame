# Generated by Django 4.1.3 on 2022-11-25 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0005_owner_created_by_person_created_by_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="persontopersonaction",
            name="other_person",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="second_person",
                to="poll.person",
            ),
        ),
        migrations.AlterField(
            model_name="persontopersonaction",
            name="person",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="first_person",
                to="poll.person",
            ),
        ),
    ]
