# Generated by Django 4.1.3 on 2022-12-15 17:46

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0035_remove_person_person_name_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="owner",
            options={
                "managed": True,
                "permissions": [("special_status", "Can edit all owners")],
                "verbose_name": "Owner",
                "verbose_name_plural": "Owners",
            },
        ),
        migrations.AddField(
            model_name="person",
            name="person_name",
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.AddField(
            model_name="race",
            name="race_description",
            field=ckeditor.fields.RichTextField(
                blank=True, null=True, verbose_name="Описание"
            ),
        ),
        migrations.AddField(
            model_name="race",
            name="race_img",
            field=models.ImageField(default="media/python.png", upload_to=""),
        ),
    ]
