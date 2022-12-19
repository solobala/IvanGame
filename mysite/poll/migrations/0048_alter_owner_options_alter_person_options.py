# Generated by Django 4.1.3 on 2022-12-18 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0047_region_zone_alter_region_location_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="owner",
            options={
                "managed": True,
                "permissions": [("can_edit_owners", "Can edit all owners")],
                "verbose_name": "Owner",
                "verbose_name_plural": "Owners",
            },
        ),
        migrations.AlterModelOptions(
            name="person",
            options={
                "managed": True,
                "permissions": [("can_list_persons", "Can list all persons")],
                "verbose_name": "Person",
                "verbose_name_plural": "Persons",
            },
        ),
    ]
