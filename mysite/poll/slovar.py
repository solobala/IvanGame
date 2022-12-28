dict_points = {
    "SP": "Стамина",
    "MP": "Колдовство",
    "IP": 'Интеллект',
    "PP": 'Сила',
    "AP": 'Ловкость',
    "FP": 'Вера',
    "LP": 'Удача',
    "CP": 'Харизма',
    "BP": 'Рассудок'
}
dict_permissions = {
    "Fire_access": 'Пирокинектика',
    "Water_access": 'Гидрософистика',
    "Wind_access": 'Аэрософистика',
    "Dirt_access": 'Геомантия',
    "Lightning_access": 'Киловактика',
    "Holy_access": 'Элафристика',
    "Curse_access": 'Катифристика',
    "Bleed_access": 'Гематомантия',
    "Nature_access": 'Ботаника',
    "Mental_access": 'Псифистика',
    "Twohanded_access": 'Владение навыками Двуручного оружия',
    "Polearm_access": 'Владение навыками Древкового оружия',
    "Onehanded_access": 'Владение навыками Одноручного оружия',
    "Stabbing_access": 'Владение навыками Колющего оружия',
    "Cutting_access": 'Владение навыками Режущего оружия',
    "Crushing_access": 'Владение навыками Дробящего оружия',
    "Small_arms_access": 'Владение навыками Стрелкового оружия',
    "Shields_access": 'Владение навыками Щитов'
}
dict_resistances = {
    "fire_res": 'Устойчивость к огню',
    "water_res": 'Устойчивость к воде',
    "wind_res": 'Устойчивость к воздуху',
    "dirt_res": 'Устойчивость к земле',
    "lightning_res": 'Устойчивость к молниям',
    "holy_res": 'Устойчивость к свету',
    "curse_res": 'Устойчивость ко тьме',
    "crush_res": 'Устойчивость к дроблению',
    "cut_res": 'Устойчивость к порезам',
    "stab_res": 'Устойчивость к протыканию'
}

dict_equipment = {
    "helmet_status": 'Шлем',
    "chest_status": 'Нагрудник',
    "shoes_status": 'Сапоги',
    "gloves_status": 'Наручи',
    "item_status": 'Прочее'
}

dict_points_start = {
    "SP_START": "Стамина",
    "MP_START": "Колдовство",
    "IP_START": 'Интеллект',
    "PP_START": 'Сила',
    "AP_START": 'Ловкость',
    "FP_START": 'Вера',
    "LP_START": 'Удача',
    "CP_START": 'Харизма',
    "BP_START": 'Рассудок'
}

dict_points_max = {
    "SP_MAX": "Стамина",
    "MP_MAX": "Колдовство",
    "IP_MAX": 'Интеллект',
    "PP_MAX": 'Сила',
    "AP_MAX": 'Ловкость',
    "FP_MAX": 'Вера',
    "LP_MAX": 'Удача',
    "CP_MAX": 'Харизма',
    "BP_MAX": 'Рассудок'
}
dict_permissions_start = {
    "Fire_access_start": 'Пирокинектика',
    "Water_access_start": 'Гидрософистика',
    "Wind_access_start": 'Аэрософистика',
    "Dirt_access_start": 'Геомантия',
    "Lightning_access_start": 'Киловактика',
    "Holy_access_start": 'Элафристика',
    "Curse_access_start": 'Катифристика',
    "Bleed_access_start": 'Гематомантия',
    "Nature_access_start": 'Ботаника',
    "Mental_access_start": 'Псифистика',
    "Twohanded_access_start": 'Владение навыками Двуручного оружия',
    "Polearm_access_start": 'Владение навыками Древкового оружия',
    "Onehanded_access_start": 'Владение навыками Одноручного оружия',
    "Stabbing_access_start": 'Владение навыками Колющего оружия',
    "Cutting_access_start": 'Владение навыками Режущего оружия',
    "Crushing_access_start": 'Владение навыками Дробящего оружия',
    "Small_arms_access_start": 'Владение навыками Стрелкового оружия',
    "Shields_access_start": 'Владение навыками Щитов'
}
dict_resistances_start = {
    "fire_res_start": 'Устойчивость к огню',
    "water_res_start": 'Устойчивость к воде',
    "wind_res_start": 'Устойчивость к воздуху',
    "dirt_res_start": 'Устойчивость к земле',
    "lightning_res_start": 'Устойчивость к молниям',
    "holy_res_start": 'Устойчивость к свету',
    "curse_res_start": 'Устойчивость ко тьме',
    "crush_res_start": 'Устойчивость к дроблению',
    "cut_res_start": 'Устойчивость к порезам',
    "stab_res_start": 'Устойчивость к протыканию'
}
dict_equipment_start = {
    "HELMET_STATUS_START": 'Шлем',
    "CHEST_STATUS_START": 'Нагрудник',
    "SHOES_STATUS_START": 'Сапоги',
    "GLOVES_STATUS_START": 'Наручи',
    "ITEM_SLOT_START": 'Прочее'
}
mypoints = dict()
for key in dict_points.keys():
    mypoints[key] = 0