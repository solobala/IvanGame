# Generated by Django 4.1.3 on 2022-12-12 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0024_rename_lightning_accesst_action_lightning_access_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="action", old_name="Polearm_acces", new_name="Polearm_access",
        ),
        migrations.RenameField(
            model_name="action",
            old_name="Small_arms_acces",
            new_name="Small_arms_access",
        ),
        migrations.RenameField(
            model_name="action",
            old_name="action_resistanses",
            new_name="action_resistances",
        ),
    ]
