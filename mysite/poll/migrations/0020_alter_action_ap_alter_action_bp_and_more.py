# Generated by Django 4.1.3 on 2022-12-12 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0019_action_ap_action_bp_action_bleed_access_action_cp_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="action",
            name="AP",
            field=models.IntegerField(default=0, verbose_name="Ловкость"),
        ),
        migrations.AlterField(
            model_name="action",
            name="BP",
            field=models.IntegerField(default=0, verbose_name="Рассудок"),
        ),
        migrations.AlterField(
            model_name="action",
            name="Bleed_access",
            field=models.IntegerField(default=0, verbose_name="Гематомантия"),
        ),
        migrations.AlterField(
            model_name="action",
            name="CP",
            field=models.IntegerField(default=0, verbose_name="Харизма"),
        ),
        migrations.AlterField(
            model_name="action",
            name="Crushing_access",
            field=models.IntegerField(
                default=0, verbose_name="Владение навыками Дробящего оружия"
            ),
        ),
        migrations.AlterField(
            model_name="action",
            name="Curse_access",
            field=models.IntegerField(default=0, verbose_name="Катифристика"),
        ),
        migrations.AlterField(
            model_name="action",
            name="Cutting_access",
            field=models.IntegerField(
                default=0, verbose_name="Владение навыками Режущего оружия"
            ),
        ),
        migrations.AlterField(
            model_name="action",
            name="Dirt_access",
            field=models.IntegerField(default=0, verbose_name="Геомантия"),
        ),
        migrations.AlterField(
            model_name="action",
            name="FP",
            field=models.IntegerField(default=0, verbose_name="Вера"),
        ),
        migrations.AlterField(
            model_name="action",
            name="Fire_access",
            field=models.IntegerField(default=0, verbose_name="Пирокинектика"),
        ),
        migrations.AlterField(
            model_name="action",
            name="Holy_access",
            field=models.IntegerField(default=0, verbose_name="Элафристика"),
        ),
        migrations.AlterField(
            model_name="action",
            name="IP",
            field=models.IntegerField(default=0, verbose_name="Интеллект"),
        ),
        migrations.AlterField(
            model_name="action",
            name="LP",
            field=models.IntegerField(default=0, verbose_name="Удача"),
        ),
        migrations.AlterField(
            model_name="action",
            name="Lightning_accesst",
            field=models.IntegerField(default=0, verbose_name="Киловактика"),
        ),
        migrations.AlterField(
            model_name="action",
            name="MP",
            field=models.IntegerField(default=0, verbose_name="Колдовство"),
        ),
        migrations.AlterField(
            model_name="action",
            name="Mental_access",
            field=models.IntegerField(default=0, verbose_name="Псифистика"),
        ),
        migrations.AlterField(
            model_name="action",
            name="Nature_access",
            field=models.IntegerField(default=0, verbose_name="Ботаника"),
        ),
        migrations.AlterField(
            model_name="action",
            name="Onehanded_access",
            field=models.IntegerField(
                default=0, verbose_name="Владение навыками Одноручного оружия"
            ),
        ),
        migrations.AlterField(
            model_name="action",
            name="PP",
            field=models.IntegerField(default=0, verbose_name="Сила"),
        ),
        migrations.AlterField(
            model_name="action",
            name="Polearm_acces",
            field=models.IntegerField(
                default=0, verbose_name="Владение навыками Древкового оружия"
            ),
        ),
        migrations.AlterField(
            model_name="action",
            name="SP",
            field=models.IntegerField(default=0, verbose_name="Стамина"),
        ),
        migrations.AlterField(
            model_name="action",
            name="Shields_access",
            field=models.IntegerField(
                default=0, verbose_name="Владение навыками Щитов"
            ),
        ),
        migrations.AlterField(
            model_name="action",
            name="Small_arms_acces",
            field=models.IntegerField(
                default=0, verbose_name="Владение навыками Стрелкового оружия"
            ),
        ),
        migrations.AlterField(
            model_name="action",
            name="Stabbing_accesst",
            field=models.IntegerField(
                default=0, verbose_name="Владение навыками Колющего оружия"
            ),
        ),
        migrations.AlterField(
            model_name="action",
            name="Twohanded_access",
            field=models.IntegerField(
                default=0, verbose_name="Владение навыками Двуручного оружия"
            ),
        ),
        migrations.AlterField(
            model_name="action",
            name="Water_access",
            field=models.IntegerField(default=0, verbose_name="Гидрософистика"),
        ),
        migrations.AlterField(
            model_name="action",
            name="Wind_access",
            field=models.IntegerField(default=0, verbose_name="Аэрософистика"),
        ),
        migrations.AlterField(
            model_name="action",
            name="chest_status",
            field=models.IntegerField(default=0, verbose_name="Нагрудник"),
        ),
        migrations.AlterField(
            model_name="action",
            name="crush_res",
            field=models.IntegerField(
                default=0, verbose_name="Сопротивляемость дроблению"
            ),
        ),
        migrations.AlterField(
            model_name="action",
            name="curse_res",
            field=models.IntegerField(default=0, verbose_name="Сопротивляемость тьме"),
        ),
        migrations.AlterField(
            model_name="action",
            name="cut_res",
            field=models.IntegerField(
                default=0, verbose_name="Сопротивляемость порезам"
            ),
        ),
        migrations.AlterField(
            model_name="action",
            name="dirt_res",
            field=models.IntegerField(default=0, verbose_name="Сопротивляемость земле"),
        ),
        migrations.AlterField(
            model_name="action",
            name="fire_res",
            field=models.IntegerField(default=0, verbose_name="Сопротивляемость огню"),
        ),
        migrations.AlterField(
            model_name="action",
            name="gloves_status",
            field=models.IntegerField(default=0, verbose_name="Наручи"),
        ),
        migrations.AlterField(
            model_name="action",
            name="helmet_status",
            field=models.IntegerField(default=0, verbose_name="Шлем"),
        ),
        migrations.AlterField(
            model_name="action",
            name="holy_res",
            field=models.IntegerField(default=0, verbose_name="Сопротивляемость свету"),
        ),
        migrations.AlterField(
            model_name="action",
            name="item_status",
            field=models.IntegerField(default=0, verbose_name="Прочее"),
        ),
        migrations.AlterField(
            model_name="action",
            name="lightning_rest",
            field=models.IntegerField(
                default=0, verbose_name="Сопротивляемость молниям"
            ),
        ),
        migrations.AlterField(
            model_name="action",
            name="shoes_status",
            field=models.IntegerField(default=0, verbose_name="Сапоги"),
        ),
        migrations.AlterField(
            model_name="action",
            name="stab_res",
            field=models.IntegerField(
                default=0, verbose_name="Сопротивляемость протыканию"
            ),
        ),
        migrations.AlterField(
            model_name="action",
            name="water_res",
            field=models.IntegerField(default=0, verbose_name="Сопротивляемость воде"),
        ),
        migrations.AlterField(
            model_name="action",
            name="wind_res",
            field=models.IntegerField(default=0, verbose_name="Сопротивляемость ветру"),
        ),
    ]
