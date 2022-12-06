# Generated by Django 4.1.3 on 2022-12-06 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0024_fraction_location_quest_personlocation_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="clan",
            options={
                "managed": True,
                "verbose_name": "Clan",
                "verbose_name_plural": "Clans",
            },
        ),
        migrations.AlterModelOptions(
            name="fraction",
            options={
                "managed": True,
                "verbose_name": "Fraction",
                "verbose_name_plural": "Fractions",
            },
        ),
        migrations.AlterModelOptions(
            name="location",
            options={
                "managed": True,
                "ordering": ["location_name"],
                "verbose_name": "Location",
                "verbose_name_plural": "Locations",
            },
        ),
        migrations.AlterModelOptions(
            name="owner",
            options={
                "managed": True,
                "verbose_name": "Owner",
                "verbose_name_plural": "Owners",
            },
        ),
        migrations.AlterModelOptions(
            name="party",
            options={
                "managed": True,
                "verbose_name": "Party",
                "verbose_name_plural": "Parties",
            },
        ),
        migrations.AlterModelOptions(
            name="person",
            options={
                "managed": True,
                "verbose_name": "Person",
                "verbose_name_plural": "Persons",
            },
        ),
        migrations.AlterModelOptions(
            name="quest",
            options={
                "managed": True,
                "verbose_name": "Quest",
                "verbose_name_plural": "Quests",
            },
        ),
        migrations.AlterModelOptions(
            name="race",
            options={
                "managed": True,
                "ordering": ["race_name"],
                "verbose_name": "Race",
                "verbose_name_plural": "Races",
            },
        ),
    ]
