# Generated by Django 4.1.3 on 2023-01-18 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0078_alter_action_action_type_alter_history_action_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="owner",
            name="owner_img",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="media/euploads",
                verbose_name="Изображение",
            ),
        ),
    ]