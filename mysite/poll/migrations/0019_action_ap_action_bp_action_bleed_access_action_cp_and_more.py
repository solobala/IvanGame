# Generated by Django 4.1.3 on 2022-12-11 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0018_remove_action_action_result_action_action_equipment_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="action", name="AP", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action", name="BP", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="Bleed_access",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action", name="CP", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="Crushing_access",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="Curse_access",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="Cutting_access",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="Dirt_access",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action", name="FP", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="Fire_access",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="Holy_access",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action", name="IP", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action", name="LP", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="Lightning_accesst",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action", name="MP", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="Mental_access",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="Nature_access",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="Onehanded_access",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action", name="PP", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="Polearm_acces",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action", name="SP", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="Shields_access",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="Small_arms_acces",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="Stabbing_accesst",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="Twohanded_access",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="Water_access",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="Wind_access",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="chest_status",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action", name="crush_res", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action", name="curse_res", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action", name="cut_res", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action", name="dirt_res", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action", name="fire_res", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="gloves_status",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="helmet_status",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action", name="holy_res", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="item_status",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="lightning_rest",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action",
            name="shoes_status",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action", name="stab_res", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action", name="water_res", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="action", name="wind_res", field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="action",
            name="action_equipment",
            field=models.JSONField(
                default={
                    "chest_status": 0,
                    "gloves_status": 0,
                    "helmet_status": 0,
                    "item_status": 0,
                    "shoes_status": 0,
                },
                verbose_name="Снаряжение",
            ),
        ),
        migrations.AlterField(
            model_name="action",
            name="action_permissions",
            field=models.JSONField(
                default={
                    "crush_res": 0,
                    "curse_res": 0,
                    "cut_res": 0,
                    "dirt_res": 0,
                    "fire_res": 0,
                    "holy_res": 0,
                    "lightning_rest": 0,
                    "stab_res": 0,
                    "water_res": 0,
                    "wind_res": 0,
                },
                verbose_name="Умения",
            ),
        ),
        migrations.AlterField(
            model_name="action",
            name="action_points",
            field=models.JSONField(
                default={
                    "AP": 0,
                    "BP": 0,
                    "CP": 0,
                    "FP": 0,
                    "IP": 0,
                    "LP": 0,
                    "MP": 0,
                    "PP": 0,
                    "SP": 0,
                },
                verbose_name="Характеристики",
            ),
        ),
        migrations.AlterField(
            model_name="action",
            name="action_resistanses",
            field=models.JSONField(
                default={
                    "Bleed_access": 0,
                    "Crushing_access": 0,
                    "Curse_access": 0,
                    "Cutting_access": 0,
                    "Dirt_access": 0,
                    "Fire_access": 0,
                    "Holy_access": 0,
                    "Lightning_accesst": 0,
                    "Mental_access": 0,
                    "Nature_access": 0,
                    "Onehanded_access": 0,
                    "Polearm_acces": 0,
                    "Shields_access": 0,
                    "Small_arms_acces": 0,
                    "Stabbing_accesst": 0,
                    "Twohanded_access": 0,
                    "Water_access": 0,
                    "Wind_access": 0,
                },
                verbose_name="Сопротивляемость",
            ),
        ),
    ]
