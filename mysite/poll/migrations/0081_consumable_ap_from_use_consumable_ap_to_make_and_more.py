# Generated by Django 4.1.3 on 2023-01-20 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("poll", "0080_alter_consumable_buy_price_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="consumable",
            name="ap_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Ловкость"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="ap_to_make",
            field=models.IntegerField(blank=True, null=True, verbose_name="Ловкость"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="bp_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Разум"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="bp_to_make",
            field=models.IntegerField(blank=True, null=True, verbose_name="Разум"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="cp_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Харизма"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="cp_to_make",
            field=models.IntegerField(blank=True, null=True, verbose_name="Харизма"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="crush_res",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="к дроблению"
            ),
        ),
        migrations.AddField(
            model_name="consumable",
            name="crush_res_damage",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="от дробления"
            ),
        ),
        migrations.AddField(
            model_name="consumable",
            name="curse_res",
            field=models.IntegerField(blank=True, null=True, verbose_name="ко тьме"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="curse_res_damage",
            field=models.IntegerField(blank=True, null=True, verbose_name="от тьмы"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="cut_res",
            field=models.IntegerField(blank=True, null=True, verbose_name="к порезам"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="cut_res_damage",
            field=models.IntegerField(blank=True, null=True, verbose_name="от порезов"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="dirt_res",
            field=models.IntegerField(blank=True, null=True, verbose_name="к земле"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="dirt_res_damage",
            field=models.IntegerField(blank=True, null=True, verbose_name="от земли"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="endurance",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Выносливость"
            ),
        ),
        migrations.AddField(
            model_name="consumable",
            name="fire_res",
            field=models.IntegerField(blank=True, null=True, verbose_name="к огню"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="fire_res_damage",
            field=models.IntegerField(blank=True, null=True, verbose_name="от огня"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="fp_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Вера"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="fp_to_make",
            field=models.IntegerField(blank=True, null=True, verbose_name="Вера"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="health",
            field=models.IntegerField(blank=True, null=True, verbose_name="Здоровье"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="holy_res",
            field=models.IntegerField(blank=True, null=True, verbose_name="к свету"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="holy_res_damage",
            field=models.IntegerField(blank=True, null=True, verbose_name="от света"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="hungry",
            field=models.IntegerField(blank=True, null=True, verbose_name="Голод"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="intoxication",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Интоксикация"
            ),
        ),
        migrations.AddField(
            model_name="consumable",
            name="ip_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Интеллект"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="ip_to_make",
            field=models.IntegerField(blank=True, null=True, verbose_name="Интеллект"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="lightning_res",
            field=models.IntegerField(blank=True, null=True, verbose_name="к молниям"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="lightning_res_damage",
            field=models.IntegerField(blank=True, null=True, verbose_name="от молний"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="lp_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Удача"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="lp_to_make",
            field=models.IntegerField(blank=True, null=True, verbose_name="Удача"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="mana",
            field=models.IntegerField(blank=True, null=True, verbose_name="Мана"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="mental_health",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Ментальное здоровье"
            ),
        ),
        migrations.AddField(
            model_name="consumable",
            name="mp_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Колдовство"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="mp_to_make",
            field=models.IntegerField(blank=True, null=True, verbose_name="Колдовство"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="pp_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Сила"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="pp_to_make",
            field=models.IntegerField(blank=True, null=True, verbose_name="Сила"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="sp_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Стамина"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="sp_to_make",
            field=models.IntegerField(blank=True, null=True, verbose_name="Стамина"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="stab_res",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="к протыканию"
            ),
        ),
        migrations.AddField(
            model_name="consumable",
            name="stab_res_damage",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="от протыкания"
            ),
        ),
        migrations.AddField(
            model_name="consumable",
            name="water_res",
            field=models.IntegerField(blank=True, null=True, verbose_name="к воде"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="water_res_damage",
            field=models.IntegerField(blank=True, null=True, verbose_name="от воды"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="wind_res",
            field=models.IntegerField(blank=True, null=True, verbose_name="к воздуху"),
        ),
        migrations.AddField(
            model_name="consumable",
            name="wind_res_damage",
            field=models.IntegerField(blank=True, null=True, verbose_name="от воздуха"),
        ),
        migrations.AddField(
            model_name="thing",
            name="ap_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Ловкость"),
        ),
        migrations.AddField(
            model_name="thing",
            name="ap_to_make",
            field=models.IntegerField(blank=True, null=True, verbose_name="Ловкость"),
        ),
        migrations.AddField(
            model_name="thing",
            name="ap_to_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Ловкость"),
        ),
        migrations.AddField(
            model_name="thing",
            name="bleed_access",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Гематомантия"
            ),
        ),
        migrations.AddField(
            model_name="thing",
            name="bp_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Разум"),
        ),
        migrations.AddField(
            model_name="thing",
            name="bp_to_make",
            field=models.IntegerField(blank=True, null=True, verbose_name="Разум"),
        ),
        migrations.AddField(
            model_name="thing",
            name="bp_to_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Разум"),
        ),
        migrations.AddField(
            model_name="thing",
            name="chest_status_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Нагрудник"),
        ),
        migrations.AddField(
            model_name="thing",
            name="chest_status_to_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Нагрудник"),
        ),
        migrations.AddField(
            model_name="thing",
            name="cp_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Харизма"),
        ),
        migrations.AddField(
            model_name="thing",
            name="cp_to_make",
            field=models.IntegerField(blank=True, null=True, verbose_name="Харизма"),
        ),
        migrations.AddField(
            model_name="thing",
            name="cp_to_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Харизма"),
        ),
        migrations.AddField(
            model_name="thing",
            name="crush_res",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="к дроблению"
            ),
        ),
        migrations.AddField(
            model_name="thing",
            name="crush_res_damage",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="к дроблению"
            ),
        ),
        migrations.AddField(
            model_name="thing",
            name="crushing_access",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Дробящее оружие"
            ),
        ),
        migrations.AddField(
            model_name="thing",
            name="curse_access",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Катифристика"
            ),
        ),
        migrations.AddField(
            model_name="thing",
            name="curse_res",
            field=models.IntegerField(blank=True, null=True, verbose_name="ко тьме"),
        ),
        migrations.AddField(
            model_name="thing",
            name="curse_res_damage",
            field=models.IntegerField(blank=True, null=True, verbose_name="ко тьме"),
        ),
        migrations.AddField(
            model_name="thing",
            name="cut_res",
            field=models.IntegerField(blank=True, null=True, verbose_name="к порезам"),
        ),
        migrations.AddField(
            model_name="thing",
            name="cut_res_damage",
            field=models.IntegerField(blank=True, null=True, verbose_name="к порезам"),
        ),
        migrations.AddField(
            model_name="thing",
            name="cutting_access",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Режущее оружие"
            ),
        ),
        migrations.AddField(
            model_name="thing",
            name="dirt_access",
            field=models.IntegerField(blank=True, null=True, verbose_name="Геомантия"),
        ),
        migrations.AddField(
            model_name="thing",
            name="dirt_res",
            field=models.IntegerField(blank=True, null=True, verbose_name="к земле"),
        ),
        migrations.AddField(
            model_name="thing",
            name="dirt_res_damage",
            field=models.IntegerField(blank=True, null=True, verbose_name="к земле"),
        ),
        migrations.AddField(
            model_name="thing",
            name="endurance",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Выносливость"
            ),
        ),
        migrations.AddField(
            model_name="thing",
            name="fire_access",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Пирокинектика"
            ),
        ),
        migrations.AddField(
            model_name="thing",
            name="fire_res",
            field=models.IntegerField(blank=True, null=True, verbose_name="к огню"),
        ),
        migrations.AddField(
            model_name="thing",
            name="fire_res_damage_damage",
            field=models.IntegerField(blank=True, null=True, verbose_name="к огню"),
        ),
        migrations.AddField(
            model_name="thing",
            name="fp_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Вера"),
        ),
        migrations.AddField(
            model_name="thing",
            name="fp_to_make",
            field=models.IntegerField(blank=True, null=True, verbose_name="Вера"),
        ),
        migrations.AddField(
            model_name="thing",
            name="fp_to_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Вера"),
        ),
        migrations.AddField(
            model_name="thing",
            name="gloves_status_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Наручи"),
        ),
        migrations.AddField(
            model_name="thing",
            name="gloves_status_to_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Наручи"),
        ),
        migrations.AddField(
            model_name="thing",
            name="health",
            field=models.IntegerField(blank=True, null=True, verbose_name="Здоровье"),
        ),
        migrations.AddField(
            model_name="thing",
            name="helmet_status_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Шлем"),
        ),
        migrations.AddField(
            model_name="thing",
            name="helmet_status_to_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Шлем"),
        ),
        migrations.AddField(
            model_name="thing",
            name="holy_access",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Элафристика"
            ),
        ),
        migrations.AddField(
            model_name="thing",
            name="holy_res",
            field=models.IntegerField(blank=True, null=True, verbose_name="к свету"),
        ),
        migrations.AddField(
            model_name="thing",
            name="holy_res_damage",
            field=models.IntegerField(blank=True, null=True, verbose_name="к свету"),
        ),
        migrations.AddField(
            model_name="thing",
            name="hungry",
            field=models.IntegerField(blank=True, null=True, verbose_name="Голод"),
        ),
        migrations.AddField(
            model_name="thing",
            name="intoxication",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Интоксикация"
            ),
        ),
        migrations.AddField(
            model_name="thing",
            name="ip_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Интеллект"),
        ),
        migrations.AddField(
            model_name="thing",
            name="ip_to_make",
            field=models.IntegerField(blank=True, null=True, verbose_name="Интеллект"),
        ),
        migrations.AddField(
            model_name="thing",
            name="ip_to_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Интеллект"),
        ),
        migrations.AddField(
            model_name="thing",
            name="item_status_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Щиты"),
        ),
        migrations.AddField(
            model_name="thing",
            name="item_status_to_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Щиты"),
        ),
        migrations.AddField(
            model_name="thing",
            name="lightning_access",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Киловактика"
            ),
        ),
        migrations.AddField(
            model_name="thing",
            name="lightning_res",
            field=models.IntegerField(blank=True, null=True, verbose_name="к молниям"),
        ),
        migrations.AddField(
            model_name="thing",
            name="lightning_res_damage",
            field=models.IntegerField(blank=True, null=True, verbose_name="к молниям"),
        ),
        migrations.AddField(
            model_name="thing",
            name="lp_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Удача"),
        ),
        migrations.AddField(
            model_name="thing",
            name="lp_to_make",
            field=models.IntegerField(blank=True, null=True, verbose_name="Удача"),
        ),
        migrations.AddField(
            model_name="thing",
            name="lp_to_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Удача"),
        ),
        migrations.AddField(
            model_name="thing",
            name="mana",
            field=models.IntegerField(blank=True, null=True, verbose_name="Мана"),
        ),
        migrations.AddField(
            model_name="thing",
            name="mental_access",
            field=models.IntegerField(blank=True, null=True, verbose_name="Псифистика"),
        ),
        migrations.AddField(
            model_name="thing",
            name="mental_health",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Ментальное здоровье"
            ),
        ),
        migrations.AddField(
            model_name="thing",
            name="mp_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Колдовство"),
        ),
        migrations.AddField(
            model_name="thing",
            name="mp_to_make",
            field=models.IntegerField(blank=True, null=True, verbose_name="Колдовство"),
        ),
        migrations.AddField(
            model_name="thing",
            name="mp_to_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Колдовство"),
        ),
        migrations.AddField(
            model_name="thing",
            name="nature_access",
            field=models.IntegerField(blank=True, null=True, verbose_name="Ботаника"),
        ),
        migrations.AddField(
            model_name="thing",
            name="onehanded_access",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Одноручное оружие"
            ),
        ),
        migrations.AddField(
            model_name="thing",
            name="polearm_access",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Древковое оружие"
            ),
        ),
        migrations.AddField(
            model_name="thing",
            name="pp_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Сила"),
        ),
        migrations.AddField(
            model_name="thing",
            name="pp_to_make",
            field=models.IntegerField(blank=True, null=True, verbose_name="Сила"),
        ),
        migrations.AddField(
            model_name="thing",
            name="pp_to_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Сила"),
        ),
        migrations.AddField(
            model_name="thing",
            name="shields_access",
            field=models.IntegerField(blank=True, null=True, verbose_name="Щиты"),
        ),
        migrations.AddField(
            model_name="thing",
            name="shoes_status_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Сапоги"),
        ),
        migrations.AddField(
            model_name="thing",
            name="shoes_status_to_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Сапоги"),
        ),
        migrations.AddField(
            model_name="thing",
            name="small_arms_access",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Стрелковое оружие"
            ),
        ),
        migrations.AddField(
            model_name="thing",
            name="sp_from_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Стамина"),
        ),
        migrations.AddField(
            model_name="thing",
            name="sp_to_make",
            field=models.IntegerField(blank=True, null=True, verbose_name="Стамина"),
        ),
        migrations.AddField(
            model_name="thing",
            name="sp_to_use",
            field=models.IntegerField(blank=True, null=True, verbose_name="Стамина"),
        ),
        migrations.AddField(
            model_name="thing",
            name="stab_res",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="к протыканию"
            ),
        ),
        migrations.AddField(
            model_name="thing",
            name="stab_res_damage",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="к протыканию"
            ),
        ),
        migrations.AddField(
            model_name="thing",
            name="stabbing_access",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Колющее оружие"
            ),
        ),
        migrations.AddField(
            model_name="thing",
            name="twohanded_access",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Двуручное оружие"
            ),
        ),
        migrations.AddField(
            model_name="thing",
            name="water_access",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Гидрософистика"
            ),
        ),
        migrations.AddField(
            model_name="thing",
            name="water_res",
            field=models.IntegerField(blank=True, null=True, verbose_name="к воде"),
        ),
        migrations.AddField(
            model_name="thing",
            name="water_res_damage",
            field=models.IntegerField(blank=True, null=True, verbose_name="к воде"),
        ),
        migrations.AddField(
            model_name="thing",
            name="wind_access",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Аэрософистика"
            ),
        ),
        migrations.AddField(
            model_name="thing",
            name="wind_res",
            field=models.IntegerField(blank=True, null=True, verbose_name="к воздуху"),
        ),
        migrations.AddField(
            model_name="thing",
            name="wind_res_damage",
            field=models.IntegerField(blank=True, null=True, verbose_name="к воздуху"),
        ),
        migrations.AlterField(
            model_name="thing",
            name="conditions",
            field=models.JSONField(blank=True, null=True, verbose_name="Кондиции"),
        ),
        migrations.AlterField(
            model_name="thing",
            name="equipment_to_use",
            field=models.JSONField(
                blank=True, null=True, verbose_name="расширение слотов от применения"
            ),
        ),
    ]
