# Generated by Django 4.1.3 on 2022-12-12 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0023_alter_action_action_equipment_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="action",
            old_name="Lightning_accesst",
            new_name="Lightning_access",
        ),
        migrations.RenameField(
            model_name="action",
            old_name="Stabbing_accesst",
            new_name="Stabbing_access",
        ),
        migrations.RenameField(
            model_name="action", old_name="lightning_rest", new_name="lightning_res",
        ),
    ]
