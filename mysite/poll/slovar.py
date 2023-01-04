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
    "Twohanded_access": 'Двуручное оружие',
    "Polearm_access": 'Древковое оружие',
    "Onehanded_access": 'Одноручное оружие',
    "Stabbing_access": 'Колющее оружие',
    "Cutting_access": 'Режущее оружие',
    "Crushing_access": 'Дробящее оружие',
    "Small_arms_access": 'Стрелковое оружие',
    "Shields_access": 'Щиты'
}
dict_resistances = {
    "fire_res": 'к огню',
    "water_res": 'к воде',
    "wind_res": 'к воздуху',
    "dirt_res": 'к земле',
    "lightning_res": 'к молниям',
    "holy_res": 'к свету',
    "curse_res": 'ко тьме',
    "crush_res": 'к дроблению',
    "cut_res": 'к порезам',
    "stab_res": 'к протыканию'
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
    "Twohanded_access_start": 'Двуручное оружие',
    "Polearm_access_start": 'Древковое оружие',
    "Onehanded_access_start": 'Одноручное оружие',
    "Stabbing_access_start": 'Колющее оружие',
    "Cutting_access_start": 'Режущее оружие',
    "Crushing_access_start": 'Дробящее оружие',
    "Small_arms_access_start": 'Стрелковое оружие',
    "Shields_access_start": 'Щиты'
}
dict_resistances_start = {
    "fire_res_start": 'к огню',
    "water_res_start": 'к воде',
    "wind_res_start": 'к воздуху',
    "dirt_res_start": 'к земле',
    "lightning_res_start": 'к молниям',
    "holy_res_start": 'к свету',
    "curse_res_start": 'ко тьме',
    "crush_res_start": 'к дроблению',
    "cut_res_start": 'к порезам',
    "stab_res_start": 'к протыканию'
}
dict_equipment_start = {
    "HELMET_STATUS_START": 'Шлем',
    "CHEST_STATUS_START": 'Нагрудник',
    "SHOES_STATUS_START": 'Сапоги',
    "GLOVES_STATUS_START": 'Наручи',
    "ITEM_SLOT_START": 'Прочее'
}
dict_conditions = {
    "health": 'Здоровье',
    "mental_health": 'Ментальное здоровье',
    "endurance": 'Выносливость',
    "mana": 'Мана',
    "hungry": 'Голод',
    "intoxication": 'Интоксикация',
    "load_capacity": 'Переносимый вес',
    "avg_magic_resistance": 'Устойчивость к маг. урону',
    "avg_physic_resistance": 'Устойчивость к физ. урону'

}
mypoints = dict()
for key in dict_points.keys():
    mypoints[key] = 0

