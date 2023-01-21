import json

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.db.models import Sum

# Create your models here.
from . import slovar


class Owner(models.Model):
    """
    Класс Игрок - владелец Персонажа (Person).
    owner_status - текущий статус FREE/BUSY- определяется по наличию у Игрока Персонажа со статусом FREE

    """

    class Status(models.TextChoices):
        FREE = '0', 'Free'
        BUSY = '1', 'Busy',
        WITHOUT = ' ', 'Без статуса'

    def is_upperclass(self):
        return self.owner_status in {
            self.Status.FREE,
            self.Status.WITHOUT,
            self.Status.BUSY,
        }

    owner_name = models.CharField('Игрок', max_length=45, blank=True, null=True)
    owner_description = RichTextField('Описание', max_length=200, blank=True, null=True)
    link = models.URLField('Ссылка', max_length=9, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    owner_status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.WITHOUT,)
    owner_img = models.ImageField('Изображение', upload_to='media/euploads', blank=True,  null=True)

    def __str__(self):

        return "%s" % self.owner_name

    def get_absolute_url(self):
        return f"/owners/{self.pk}/"
        # return reverse('poll:owner-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        # возвращает объект Owner с добавленным owner_status
        try:
            if not self.person_set.all().filter(status=1).exists():
                self.owner_status = self.Status.BUSY
            else:
                self.owner_status = self.Status.FREE
        except ValueError:
            pass
        super().save(*args, **kwargs)

    @property
    def full_link(self):
        """Возвращает ссылку"""
        self.link = 'https://vk.com/id' + str(self.link)
        return "%s" % self.link

    class Meta:
        managed = True
        db_table = 'owner'
        verbose_name = "Owner"
        verbose_name_plural = "Owners"
        # app_label = 'poll'
        permissions = [
            ('can_edit_owners', 'Can edit all owners'),
        ]


class Consumable(models.Model):
    """
    Расходники
    """
    consumable_name = models.CharField(verbose_name='Название', max_length=128, blank=True, null=True)
    consumable_description = RichTextField(verbose_name='Описание', blank=True, null=True)
    sale_price = models.IntegerField(verbose_name='Цена продажи', blank=True, null=True)
    buy_price = models.IntegerField(verbose_name='Цена покупки', blank=True, null=True)
    weight = models.IntegerField(verbose_name='Вес', blank=True, null=True)

    points_to_make = models.JSONField(verbose_name='очки характеристик для создания', blank=True, null=True)
    sp_to_make = models.IntegerField(verbose_name='Стамина', blank=True, null=True)
    mp_to_make = models.IntegerField(verbose_name='Колдовство', blank=True, null=True)
    ip_to_make = models.IntegerField(verbose_name='Интеллект', blank=True, null=True)
    pp_to_make = models.IntegerField(verbose_name='Сила', blank=True, null=True)
    ap_to_make = models.IntegerField(verbose_name='Ловкость', blank=True, null=True)
    fp_to_make = models.IntegerField(verbose_name='Вера', blank=True, null=True)
    lp_to_make = models.IntegerField(verbose_name='Удача', blank=True, null=True)
    cp_to_make = models.IntegerField(verbose_name='Харизма', blank=True, null=True)
    bp_to_make = models.IntegerField(verbose_name='Разум', blank=True, null=True)

    points_from_use = models.JSONField(verbose_name='очки характеристик от применения', blank=True, null=True)
    sp_from_use = models.IntegerField(verbose_name='Стамина', blank=True, null=True)
    mp_from_use = models.IntegerField(verbose_name='Колдовство', blank=True, null=True)
    ip_from_use = models.IntegerField(verbose_name='Интеллект', blank=True, null=True)
    pp_from_use = models.IntegerField(verbose_name='Сила', blank=True, null=True)
    ap_from_use = models.IntegerField(verbose_name='Ловкость', blank=True, null=True)
    fp_from_use = models.IntegerField(verbose_name='Вера', blank=True, null=True)
    lp_from_use = models.IntegerField(verbose_name='Удача', blank=True, null=True)
    cp_from_use = models.IntegerField(verbose_name='Харизма', blank=True, null=True)
    bp_from_use = models.IntegerField(verbose_name='Разум', blank=True, null=True)

    resistances_from_use = models.JSONField(verbose_name='очки сопротивлений от применения', blank=True, null=True)
    fire_res = models.IntegerField(verbose_name='к огню', blank=True, null=True)
    water_res = models.IntegerField(verbose_name='к воде', blank=True, null=True)
    wind_res = models.IntegerField(verbose_name='к воздуху', blank=True, null=True)
    dirt_res = models.IntegerField(verbose_name='к земле', blank=True, null=True)
    lightning_res = models.IntegerField(verbose_name='к молниям', blank=True, null=True)
    holy_res = models.IntegerField(verbose_name='к свету', blank=True, null=True)
    curse_res = models.IntegerField(verbose_name='ко тьме', blank=True, null=True)
    crush_res = models.IntegerField(verbose_name='к дроблению', blank=True, null=True)
    cut_res = models.IntegerField(verbose_name='к порезам', blank=True, null=True)
    stab_res = models.IntegerField(verbose_name='к протыканию', blank=True, null=True)

    conditions = models.JSONField(verbose_name='очки кондиций', blank=True, null=True)
    health = models.IntegerField(verbose_name='Здоровье', blank=True, null=True)
    mental_health = models.IntegerField(verbose_name='Ментальное здоровье', blank=True, null=True)
    endurance = models.IntegerField(verbose_name='Выносливость', blank=True, null=True)
    mana = models.IntegerField(verbose_name='Мана', blank=True, null=True)
    hungry = models.IntegerField(verbose_name='Голод', blank=True, null=True)
    intoxication = models.IntegerField(verbose_name='Интоксикация', blank=True, null=True)

    damage_from_use = models.JSONField(verbose_name='очки урона противнику от применения', blank=True, null=True)
    fire_res_damage = models.IntegerField(verbose_name='от огня', blank=True, null=True)
    water_res_damage = models.IntegerField(verbose_name='от воды', blank=True, null=True)
    wind_res_damage = models.IntegerField(verbose_name='от воздуха', blank=True, null=True)
    dirt_res_damage = models.IntegerField(verbose_name='от земли', blank=True, null=True)
    lightning_res_damage = models.IntegerField(verbose_name='от молний', blank=True, null=True)
    holy_res_damage = models.IntegerField(verbose_name='от света', blank=True, null=True)
    curse_res_damage = models.IntegerField(verbose_name='от тьмы', blank=True, null=True)
    crush_res_damage = models.IntegerField(verbose_name='от дробления', blank=True, null=True)
    cut_res_damage = models.IntegerField(verbose_name='от порезов', blank=True, null=True)
    stab_res_damage = models.IntegerField(verbose_name='от протыкания', blank=True, null=True)
    clean_damage = models.IntegerField(verbose_name='чистый урон', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'consumable'
        verbose_name = "Consumable"
        verbose_name_plural = "Consumable"
        # app_label = 'poll'

    def __str__(self):
        return "%s" % self.consumable_name

    def get_absolute_url(self):
        return reverse('poll:consumable-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        points_to_make = dict()
        points_from_use = dict()
        for key in slovar.dict_points.keys():
            points_to_make[key+'_to_make'] = self.__getattribute__(key+'_to_make')
            points_from_use[key + '_from_use'] = self.__getattribute__(key + '_from_use')
        self.__setattr__("points_to_make", json.dumps(points_to_make, indent=4))
        self.__setattr__("points_from_use", json.dumps(points_from_use, indent=4))

        resistances_from_use = dict()
        for key in slovar.dict_resistances.keys():
            resistances_from_use[key] = self.__getattribute__(key)
        self.__setattr__("resistances_from_use", json.dumps(resistances_from_use, indent=4))

        conditions = dict()
        for key in slovar.dict_conditions.keys():
            if key not in ["load_capacity", "avg_magic_resistance", "avg_physic_resistance"]:
                conditions[key] = self.__getattribute__(key)
        self.__setattr__("conditions", json.dumps(conditions, indent=4))

        damage_from_use = dict()
        for key in slovar.dict_damage.keys():
            damage_from_use[key] = self.__getattribute__(key)
        self.__setattr__("damage_from_use", json.dumps(damage_from_use, indent=4))

        super(Consumable, self).save(*args, **kwargs)

class Thing(models.Model):
    """
    артефекты
    """
    thing_name = models.CharField(verbose_name='Название', max_length=128, blank=True, null=True)
    thing_description = RichTextField(verbose_name='Описание', blank=True, null=True)
    
    points_to_make = models.JSONField(verbose_name='очки характеристик для создания', blank=True, null=True)
    sp_to_make = models.IntegerField(verbose_name='Стамина', blank=True, null=True)
    mp_to_make = models.IntegerField(verbose_name='Колдовство', blank=True, null=True)
    ip_to_make = models.IntegerField(verbose_name='Интеллект', blank=True, null=True)
    pp_to_make = models.IntegerField(verbose_name='Сила', blank=True, null=True)
    ap_to_make = models.IntegerField(verbose_name='Ловкость', blank=True, null=True)
    fp_to_make = models.IntegerField(verbose_name='Вера', blank=True, null=True)
    lp_to_make = models.IntegerField(verbose_name='Удача', blank=True, null=True)
    cp_to_make = models.IntegerField(verbose_name='Харизма', blank=True, null=True)
    bp_to_make = models.IntegerField(verbose_name='Разум', blank=True, null=True)
    
    points_to_use = models.JSONField(verbose_name='очки характеристик для применения', blank=True, null=True)
    sp_to_use = models.IntegerField(verbose_name='Стамина', blank=True, null=True)
    mp_to_use = models.IntegerField(verbose_name='Колдовство', blank=True, null=True)
    ip_to_use = models.IntegerField(verbose_name='Интеллект', blank=True, null=True)
    pp_to_use = models.IntegerField(verbose_name='Сила', blank=True, null=True)
    ap_to_use = models.IntegerField(verbose_name='Ловкость', blank=True, null=True)
    fp_to_use = models.IntegerField(verbose_name='Вера', blank=True, null=True)
    lp_to_use = models.IntegerField(verbose_name='Удача', blank=True, null=True)
    cp_to_use = models.IntegerField(verbose_name='Харизма', blank=True, null=True)
    bp_to_use = models.IntegerField(verbose_name='Разум', blank=True, null=True)
    
    points_from_use = models.JSONField(verbose_name='очки характеристик от применения', blank=True, null=True)
    sp_from_use = models.IntegerField(verbose_name='Стамина', blank=True, null=True)
    mp_from_use = models.IntegerField(verbose_name='Колдовство', blank=True, null=True)
    ip_from_use = models.IntegerField(verbose_name='Интеллект', blank=True, null=True)
    pp_from_use = models.IntegerField(verbose_name='Сила', blank=True, null=True)
    ap_from_use = models.IntegerField(verbose_name='Ловкость', blank=True, null=True)
    fp_from_use = models.IntegerField(verbose_name='Вера', blank=True, null=True)
    lp_from_use = models.IntegerField(verbose_name='Удача', blank=True, null=True)
    cp_from_use = models.IntegerField(verbose_name='Харизма', blank=True, null=True)
    bp_from_use = models.IntegerField(verbose_name='Разум', blank=True, null=True)
    
    resistances_from_use = models.JSONField(verbose_name='очки сопротивлений от применения', blank=True, null=True)
    fire_res = models.IntegerField(verbose_name='к огню', blank=True, null=True)
    water_res = models.IntegerField(verbose_name='к воде', blank=True, null=True)
    wind_res = models.IntegerField(verbose_name='к воздуху', blank=True, null=True)
    dirt_res = models.IntegerField(verbose_name='к земле', blank=True, null=True)
    lightning_res = models.IntegerField(verbose_name='к молниям', blank=True, null=True)
    holy_res = models.IntegerField(verbose_name='к свету', blank=True, null=True)
    curse_res = models.IntegerField(verbose_name='ко тьме', blank=True, null=True)
    crush_res = models.IntegerField(verbose_name='к дроблению', blank=True, null=True)
    cut_res = models.IntegerField(verbose_name='к порезам', blank=True, null=True)
    stab_res = models.IntegerField(verbose_name='к протыканию', blank=True, null=True)
    
    permissions_from_use = models.JSONField(verbose_name='очки навыков от применения', blank=True, null=True)
    fire_access = models.IntegerField(verbose_name='Пирокинектика', blank=True, null=True)
    water_access = models.IntegerField(verbose_name='Гидрософистика', blank=True, null=True)
    wind_access = models.IntegerField(verbose_name='Аэрософистика', blank=True, null=True)
    dirt_access = models.IntegerField(verbose_name='Геомантия', blank=True, null=True)
    lightning_access = models.IntegerField(verbose_name='Киловактика', blank=True, null=True)
    holy_access = models.IntegerField(verbose_name='Элафристика', blank=True, null=True)
    curse_access = models.IntegerField(verbose_name='Катифристика', blank=True, null=True)
    bleed_access = models.IntegerField(verbose_name='Гематомантия', blank=True, null=True)
    nature_access = models.IntegerField(verbose_name='Ботаника', blank=True, null=True)
    mental_access = models.IntegerField(verbose_name='Псифистика', blank=True, null=True)
    twohanded_access = models.IntegerField(verbose_name='Двуручное оружие', blank=True, null=True)
    polearm_access = models.IntegerField(verbose_name='Древковое оружие', blank=True, null=True)
    onehanded_access = models.IntegerField(verbose_name='Одноручное оружие', blank=True, null=True)
    stabbing_access = models.IntegerField(verbose_name='Колющее оружие', blank=True, null=True)
    cutting_access = models.IntegerField(verbose_name='Режущее оружие', blank=True, null=True)
    crushing_access = models.IntegerField(verbose_name='Дробящее оружие', blank=True, null=True)
    small_arms_access = models.IntegerField(verbose_name='Стрелковое оружие', blank=True, null=True)
    shields_access = models.IntegerField(verbose_name='Щиты', blank=True, null=True)
    
    equipment_to_use = models.JSONField(verbose_name='расширение слотов от применения', blank=True, null=True)
    helmet_status_to_use = models.IntegerField(verbose_name='Шлем', blank=True, null=True)
    chest_status_to_use = models.IntegerField(verbose_name='Нагрудник', blank=True, null=True)
    shoes_status_to_use = models.IntegerField(verbose_name='Сапоги', blank=True, null=True)
    gloves_status_to_use = models.IntegerField(verbose_name='Наручи', blank=True, null=True)
    item_status_to_use = models.IntegerField(verbose_name='Щиты', blank=True, null=True)

    equipment_from_use = models.JSONField(verbose_name='расширение слотов от применения', blank=True, null=True)
    helmet_status_from_use = models.IntegerField(verbose_name='Шлем', blank=True, null=True)
    chest_status_from_use = models.IntegerField(verbose_name='Нагрудник', blank=True, null=True)
    shoes_status_from_use = models.IntegerField(verbose_name='Сапоги', blank=True, null=True)
    gloves_status_from_use = models.IntegerField(verbose_name='Наручи', blank=True, null=True)
    item_status_from_use = models.IntegerField(verbose_name='Щиты', blank=True, null=True)
    
    conditions = models.JSONField(verbose_name='Кондиции', blank=True, null=True)
    health = models.IntegerField(verbose_name='Здоровье', blank=True, null=True)
    mental_health = models.IntegerField(verbose_name='Ментальное здоровье', blank=True, null=True)
    endurance = models.IntegerField(verbose_name='Выносливость', blank=True, null=True)
    mana = models.IntegerField(verbose_name='Мана', blank=True, null=True)
    hungry = models.IntegerField(verbose_name='Голод', blank=True, null=True)
    intoxication = models.IntegerField(verbose_name='Интоксикация', blank=True, null=True)
   
    damage_from_use = models.JSONField(verbose_name='очки урона противнику от применения', blank=True, null=True)
    fire_res_damage_damage = models.IntegerField(verbose_name='к огню', blank=True, null=True)
    water_res_damage = models.IntegerField(verbose_name='к воде', blank=True, null=True)
    wind_res_damage = models.IntegerField(verbose_name='к воздуху', blank=True, null=True)
    dirt_res_damage = models.IntegerField(verbose_name='к земле', blank=True, null=True)
    lightning_res_damage = models.IntegerField(verbose_name='к молниям', blank=True, null=True)
    holy_res_damage = models.IntegerField(verbose_name='к свету', blank=True, null=True)
    curse_res_damage = models.IntegerField(verbose_name='ко тьме', blank=True, null=True)
    crush_res_damage = models.IntegerField(verbose_name='к дроблению', blank=True, null=True)
    cut_res_damage = models.IntegerField(verbose_name='к порезам', blank=True, null=True)
    stab_res_damage = models.IntegerField(verbose_name='к протыканию', blank=True, null=True)
    clean_damage = models.IntegerField(verbose_name='чистый урон', blank=True, null=True)
    sale_price = models.IntegerField(verbose_name='Цена продажи', default=100)
    buy_price = models.IntegerField(verbose_name='Цена покупки', default=100)
    weight = models.IntegerField(verbose_name='Вес', default=0)

    class Meta:
        managed = True
        db_table = 'thing'
        verbose_name = "Thing"
        verbose_name_plural = "Things"
        # app_label = 'poll'

    def __str__(self):
        return "%s" % self.thing_name

    def get_absolute_url(self):
        return reverse('poll:thing-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Thing, self).save(*args, **kwargs)


class Info(models.Model):
    agg_points = models.IntegerField(verbose_name='Агрегированные очки', default=0)
    points = models.JSONField(verbose_name='Характеристики', blank=True, null=True)
    sp = models.IntegerField(verbose_name="Стамина", default=0)
    mp = models.IntegerField(verbose_name="Колдовство", default=0)
    ip = models.IntegerField(verbose_name="Интеллект", default=0)
    pp = models.IntegerField(verbose_name="Сила", default=0)
    ap = models.IntegerField(verbose_name="Ловкость", default=0)
    fp = models.IntegerField(verbose_name="Вера", default=0)
    lp = models.IntegerField(verbose_name="Удача", default=0)
    cp = models.IntegerField(verbose_name="Харизма", default=0)
    bp = models.IntegerField(verbose_name="Рассудок", default=0)

    resistances = models.JSONField(verbose_name='Устойчивость', blank=True, null=True)
    fire_res = models.IntegerField(verbose_name="к огню", default=0)
    water_res = models.IntegerField(verbose_name="к воде", default=0)
    wind_res = models.IntegerField(verbose_name="к ветру", default=0)
    dirt_res = models.IntegerField(verbose_name="к земле", default=0)
    lightning_res = models.IntegerField(verbose_name="к молниям", default=0)
    holy_res = models.IntegerField(verbose_name="к свету", default=0)
    curse_res = models.IntegerField(verbose_name="к тьме", default=0)
    crush_res = models.IntegerField(verbose_name="к дроблению", default=0)
    cut_res = models.IntegerField(verbose_name="к порезам", default=0)
    stab_res = models.IntegerField(verbose_name="к протыканию", default=0)

    permissions = models.JSONField(verbose_name='Навыки', blank=True, null=True)
    fire_access = models.IntegerField(verbose_name="Пирокинектика", default=0)
    water_access = models.IntegerField(verbose_name="Гидрософистика", default=0)
    wind_access = models.IntegerField(verbose_name="Аэрософистика", default=0)
    dirt_access = models.IntegerField(verbose_name="Геомантия", default=0)
    lightning_access = models.IntegerField(verbose_name="Киловактика", default=0)
    holy_access = models.IntegerField(verbose_name="Элафристика", default=0)
    curse_access = models.IntegerField(verbose_name="Катифристика", default=0)
    bleed_access = models.IntegerField(verbose_name="Гематомантия", default=0)
    nature_access = models.IntegerField(verbose_name="Ботаника", default=0)
    mental_access = models.IntegerField(verbose_name="Псифистика", default=0)
    twohanded_access = models.IntegerField(verbose_name="Двуручное оружие", default=0)
    polearm_access = models.IntegerField(verbose_name="Древковое оружие", default=0)
    onehanded_access = models.IntegerField(verbose_name="Одноручное оружие", default=0)
    stabbing_access = models.IntegerField(verbose_name="Колющее оружие", default=0)
    cutting_access = models.IntegerField(verbose_name="Режущее оружие", default=0)
    crushing_access = models.IntegerField(verbose_name="Дробящее оружие", default=0)
    small_arms_access = models.IntegerField(verbose_name="Стрелковое оружие", default=0)
    shields_access = models.IntegerField(verbose_name="Щиты", default=0)

    equipment = models.JSONField(verbose_name='Снаряжение', blank=True, null=True)
    helmet_status = models.IntegerField(verbose_name='Шлем', default=0)
    chest_status = models.IntegerField(verbose_name='Нагрудник', default=0)
    shoes_status = models.IntegerField(verbose_name='Сапоги', default=0)
    gloves_status = models.IntegerField(verbose_name='Наручи', default=0)
    item_status = models.IntegerField(verbose_name='Прочее', default=0)

    fov = models.IntegerField(verbose_name='Область обзора', default=0)
    rov = models.IntegerField(verbose_name='Дальность обзора', default=0)
    level = models.IntegerField(verbose_name='Уровень', default=0)

    class Meta:
        abstract = True


class Feature(Info):

    feature_name = models.CharField(verbose_name='Название', max_length=128, blank=True, null=True)
    feature_description = RichTextField(verbose_name='Описание', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'feature'
        verbose_name = "Feature"
        verbose_name_plural = "Features"
        # app_label = 'poll'

    def __str__(self):
        return "%s" % self.feature_name

    def get_absolute_url(self):
        return reverse('poll:feature-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        points = dict()
        for key in slovar.dict_points.keys():
            points[key] = self.__getattribute__(key)
        self.__setattr__("points", json.dumps(points, indent=4))

        permissions = dict()
        for key in slovar.dict_permissions.keys():
            permissions[key] = self.__getattribute__(key)
        self.__setattr__("permissions", json.dumps(points, indent=4))

        resistances = dict()
        for key in slovar.dict_resistances.keys():
            resistances[key] = self.__getattribute__(key)
        self.__setattr__("resistances", json.dumps(points, indent=4))

        equipment = dict()
        for key in slovar.dict_equipment.keys():
            equipment[key] = self.__getattribute__(key)
        self.__setattr__("equipment", json.dumps(points, indent=4))

        super(Feature, self).save(*args, **kwargs)


class Race(models.Model):
    """
    Класс Раса  Персонажа (Person).
  `race_name` varchar(45) NOT NULL COMMENT 'Наименование расы персонажа',
  `race_description` varchar(200) DEFAULT NULL COMMENT 'Описание возможностей расы персонажа',
  `start_points` json DEFAULT NULL COMMENT 'стартовые  значение очков стамины, маны, интелекта, силы, ловкости, веры,
  удачи, харизмы и рассудка в формате JSON',
  `finish_points` json DEFAULT NULL COMMENT 'финишные значение очков стамины, маны, интелекта, силы, ловкости, веры,
  удачи, харизмы и рассудка в формате JSON',
  `start_resistances` json DEFAULT NULL COMMENT 'стартовые значение устойчивости к воздействию водой, огнем, ветром ,
  `start_permissions` json DEFAULT NULL COMMENT 'стартовые значение разрешений на воздействие водой, огнем, ветром ',
  equipment json снаряжение json DEFAULT NULL COMMENT 'Стартовые значения количества слотов для экипировки',
  PRIMARY KEY (`race_id`)
    """

    class Races(models.TextChoices):
        ELF = '0', 'Эльф',
        ANGEL = '1', 'Ангел',
        PHOENIX = '2', 'Феникс',
        DRIADE = '3', 'Дриада',
        DEMON = '4', 'Демон',
        VAMPIRE = '5', 'Вампир',
        DROW = '6', 'Дроу',
        SHADOW = '7', 'Тень',
        ARACHNID = '8', 'Арахнид',
        UNDEAD = '9', 'Нежить',
        DRAGON = '10', 'Дракон',
        DRAGONATE = '11', 'Драконейт',
        WEREWOLF = '12', 'Оборотень',
        HUMAN = '13', 'Человек',
        DWARF = '14', 'Гном',
        RUSAL = '15', 'Русал',
        ANIMAL = '16', 'Зверин',
        BESTIAL = '17', 'Звероподобное',
        KITES = '18', 'Змеелюд',
        METHAMORPH = '19', 'Метаморф',
        ATHLANT = '20', 'Атлант',
        GOBLIN = '21', 'Гоблин',
        ORK = '22', 'Орк',
        OTHER = '23', 'прочие'

    def is_upperclass(self):
        return self.race_name in {
            self.Races.ELF,
            self.Races.ANGEL,
            self.Races.PHOENIX,
            self.Races.DRIADE,
            self.Races.DEMON,
            self.Races.VAMPIRE,
            self.Races.DROW,
            self.Races.SHADOW,
            self.Races.ARACHNID,
            self.Races.UNDEAD,
            self.Races.DRAGON,
            self.Races.DRAGONATE,
            self.Races.WEREWOLF,
            self.Races.HUMAN,
            self.Races.DWARF,
            self.Races.RUSAL,
            self.Races.ANIMAL,
            self.Races.BESTIAL,
            self.Races.KITES,
            self.Races.METHAMORPH,
            self.Races.ATHLANT,
            self.Races.GOBLIN,
            self.Races.ORK,
            self.Races.OTHER
        }

    race_name = models.CharField('Раса', max_length=20, choices=Races.choices, default=Races.HUMAN)
    race_description = RichTextField('Описание',  blank=True, null=True)
    race_img = models.ImageField('Изображение', default='media/python.png')
    lifetime = models.IntegerField('Продолжительность жизни',  default=100)
    start_points = models.JSONField('Стартовые характеристики')
    finish_points = models.JSONField('Максимальные характеристики')
    start_resistances = models.JSONField('Устойчивость')
    start_permissions = models.JSONField('Навыки')
    equipment = models.JSONField('Снаряжение')
    fov = models.IntegerField('Область обзора',  default=0)
    rov = models.IntegerField('Дальность обзора',  default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "%s" % (
            self.get_race_name_display(),

        )

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/races/{self.pk}/"
        # return reverse('poll:race-detail', kwargs={'pk': self.pk})

    class Meta:
        managed = True
        db_table = 'race'
        ordering = ['race_name']
        verbose_name = "Race"
        verbose_name_plural = "Races"
        # app_label = 'poll'


class Person(models.Model):
    class Status(models.IntegerChoices):
        FREEZED = 0
        FREE = 1
        BUSY = 2

    def is_upperclass(self):
        return self.status in {
            self.Status.FREE,
            self.Status.BUSY,
            self.Status.FREEZED
        }

    person_name = models.CharField('Персонаж', max_length=45, blank=True, null=True)
    person_img = models.ImageField('Изображение', default='media/euploads/python.png')
    owner = models.ForeignKey('Owner', verbose_name='Владелец', on_delete=models.CASCADE, blank=True, null=True)
    link = models.CharField('Ссылка', max_length=30, blank=True, null=True)
    biography = RichTextField('Биография', blank=True, null=True)
    character = RichTextField('Характер', blank=True, null=True)
    interests = RichTextField('Интересы', blank=True, null=True)
    phobias = RichTextField('Фобии', blank=True, null=True)
    race = models.ForeignKey('Race', verbose_name='Раса', on_delete=models.CASCADE, null=True)
    location_birth = models.ForeignKey('Location', verbose_name='Место возрождения', related_name='location_birth',
                                       on_delete=models.CASCADE, blank=True, null=True)
    birth_date = models.DateTimeField('Дата рождения', blank=True, null=True)
    location_death = models.ForeignKey('Location', verbose_name='Место гибели', related_name='location_death', on_delete=models.CASCADE, blank=True, null=True)
    death_date = models.DateTimeField('Дата гибели', blank=True, null=True)
    status = models.IntegerField('Статус', choices=Status.choices, default=Status.FREE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    features = models.ManyToManyField(Feature)

    # free = FreePersonManager()
    # busy = BusyPersonManager()
    # freezed = FreezedPersonManager()

    def __str__(self):
        return self.person_name

    def get_absolute_url(self):
        return f"/persons/{self.pk}/"
        #  return reverse('poll:person-detail', kwargs={'pk': self.pk})

    class Meta:
        managed = True
        db_table = 'person'
        verbose_name = "Person"
        verbose_name_plural = "Persons"
        permissions = [
            ('can_list_persons', 'Can list all persons'),
        ]
        # app_label = 'poll'


class Zone(models.Model):
    zone_name = models.CharField('Название', max_length=128, blank=True, null=True)
    zone_description = RichTextField(verbose_name='Описание', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'zone'
        verbose_name = "zone"
        verbose_name_plural = "Zones"
        ordering = ['zone_name']

    def __str__(self):
        return "%s" % self.zone_name

    def get_absolute_url(self):
        return reverse('poll:zone-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Location(models.Model):
    location_name = models.CharField(verbose_name='Название', max_length=128, blank=True, null=True)
    location_description = RichTextField(verbose_name='Описание', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'location'
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordering = ['location_name']

    def __str__(self):
        return "%s" % self.location_name

    def get_absolute_url(self):
        return reverse('poll:location-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Region(models.Model):
    region_name = models.CharField('Название', max_length=128, blank=True, null=True)
    region_description = RichTextField(verbose_name='Описание', blank=True, null=True)
    coordinates = models.CharField('Координаты', max_length=14, blank=True, null=True)
    x = models.IntegerField('X', blank=True, null=True)
    y = models.IntegerField('Y', blank=True, null=True)
    row = models.IntegerField('row', blank=True, null=True)
    column = models.IntegerField('column', blank=True, null=True)
    location = models.ForeignKey(Location, verbose_name='Локация', on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, verbose_name='Зона', on_delete=models.CASCADE)
    fraction = models.ForeignKey('Fraction', verbose_name='Фракция', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'region'
        verbose_name = "Region"
        verbose_name_plural = "Regions"
        ordering = ['region_name']

    def __str__(self):
        return "%s" % self.region_name

    def get_absolute_url(self):
        return reverse('poll:region-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class District(models.Model):
    district_name = models.CharField(max_length=30, blank=True, null=True)
    district_description = RichTextUploadingField(verbose_name='Описание', blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    x = models.IntegerField(blank=True, null=True)
    y = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'district'
        verbose_name = "District"
        verbose_name_plural = "Districts"
        ordering = ['district_name']

    def __str__(self):
        return "%s" % self.district_name

    def get_absolute_url(self):
        return reverse('poll:district-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Group(models.Model):
    group_name = models.CharField(max_length=128, default='group')
    members = models.ManyToManyField(
        Person,
        through='Membership',
        through_fields=('group', 'person'),
    )

    class Meta:
        managed = True
        db_table = 'group'
        # app_label = 'poll'

    def __str__(self):
        self.group_name = self.members.through.objects.filter(group__id=self.pk)[0].inviter.person_name
        if self.members.count() >= 1:
            for member in self.members.through.objects.filter(group__id=self.pk):
                self.group_name = self.group_name + '; ' + member.person.person_name
        return "%s" % self.group_name

    def get_absolute_url(self):
        #  return reverse('poll:person_detail', args=[str(self.id)])
        return reverse('poll:group-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        # возвращает объект Group с измененным group_name
        # mo.Group.objects.get(id=7).members.through.objects.filter(group__id=7) - возщвращает
        # набор membership из пар inviter-person
        # Можно получить список группы либо по person, либо по inviter либо по названию группы
        # ПОиск участников группы по  invitor -  mo.Group.objects.get(id=2).members.through.objects.
        # filter(person_id=mo.Person.objects.get(person_name='Лилит Игнис').id)
        # ПОиск участников группы по  person -  mo.Group.objects.get(id=2).members.through.objects.
        # filter(inviter_id=mo.Person.objects.get(person_name='Люцифер Вераз').id)
        try:
            # if self.members.count() >= 1:
            #     self.group_name = self.members.through.objects.filter(
            #         group__id=self.pk).inviter.person_name
            #     for member in self.members.through.objects.filter(group__id=self.pk):
            #         self.group_name = self.group_name + '; ' + member.person.person_name
            self.group_name = self.members.through.objects.filter(group__id=self.pk).inviter.person_name
            for member in self.members.through.objects.filter(group__id=self.pk):
                self.group_name = self.group_name + '; ' + member.person.person_name
        except ObjectDoesNotExist:
        #except self.members.count() == 0:
            pass
        finally:
            super().save(*args, **kwargs)


class Membership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    inviter = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="membership_invites",
    )
    invite_reason = models.CharField(max_length=64)

    class Meta:
        managed = True
        db_table = 'membership'
        # app_label = 'poll'

    def __str__(self):
        return "%s, %s" % (self.inviter, self.person)
        # return "%s, %s,  %s,  %s," % (self.group, self.person, self.inviter, self.invite_reason)

    def get_absolute_url(self):
        #  return reverse('poll:person_detail', args=[str(self.id)])
        return reverse('poll:membership', kwargs={'pk': self.pk})


class Clan(models.Model):
    clan_name = models.CharField(max_length=128, blank=True, null=True)
    clan_description = models.TextField(verbose_name='Описание', blank=True, null=True)
    chief = models.ForeignKey('Person', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'clan'
        verbose_name = "Clan"
        verbose_name_plural = "Clans"
        # app_label = 'poll'

    def __str__(self):
        return "%s" % self.clan_name

    def get_absolute_url(self):
        return reverse('poll:clan-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Fraction(models.Model):
    fraction_name = models.CharField(verbose_name='Название', max_length=128, blank=True, null=True)
    fraction_description = models.TextField(verbose_name='Описание', blank=True, null=True)

    class Meta:
        # managed = True
        db_table = 'fraction'
        verbose_name = "Fraction"
        verbose_name_plural = "Fractions"
        # app_label = 'poll'

    def __str__(self):
        return "%s" % self.fraction_name

    def get_absolute_url(self):
        return reverse('poll:fraction-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Quest(models.Model):
    quest_name = models.CharField(max_length=128, blank=True, null=True)
    quest_description = models.TextField(verbose_name='Описание', blank=True, null=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    duration = models.TimeField
    benefits = models.JSONField
    requirements = models.JSONField

    class Meta:
        managed = True
        db_table = 'quest'
        verbose_name = "Quest"
        verbose_name_plural = "Quests"
        # app_label = 'poll'

    def __str__(self):
        return "%s" % self.quest_name

    def get_absolute_url(self):
        return reverse('poll:quest-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Party(models.Model):
    party_name = models.CharField(max_length=128, blank=True, null=True)
    party_description = models.TextField(verbose_name='Описание', blank=True, null=True)
    quest = models.ForeignKey('Quest', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'party'
        verbose_name = "Party"
        verbose_name_plural = "Parties"
        # app_label = 'poll'

    def __str__(self):
        return "%s, %s" % (self.party_name, self.quest)

    def get_absolute_url(self):
        return reverse('poll:party-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class LocationFraction(models.Model):
    """
    Репутация фракций в чужих локациях

    location - чужая локация
    reputation - репутация фракции в чужой локации
    """

    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    fraction = models.ForeignKey('Fraction', on_delete=models.CASCADE)
    reputation = models.IntegerField(blank=True, null=True)

    class Meta:
        # managed = True
        db_table = 'location_fraction'

        # app_label = 'poll'

    def __str__(self):
        return "%s, %s" % (self.fraction, self.location)

    def get_absolute_url(self):
        return reverse('poll:location-fraction-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class FractionFraction(models.Model):
    """
    fraction -  фракции
    other_fraction - чужая локация
    reputation - репутация фракции у чужой фракции
    """
    fraction = models.ForeignKey('Fraction', on_delete=models.CASCADE)
    other_fraction = models.ForeignKey('Fraction', on_delete=models.CASCADE, related_name="other_fraction")
    reputation = models.IntegerField(blank=True, null=True)

    class Meta:
        # managed = True
        db_table = 'fraction_fraction'
        # app_label = 'poll'

    def __str__(self):
        return "%s, %s" % (self.fraction, self.other_fraction)

    def get_absolute_url(self):
        return reverse('poll:fraction-fraction-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class PersonFraction(models.Model):
    """
    fraction -  фракции
    person - персонаж
    reputation - репутация персонажа у чужой фракции
    """
    fraction = models.ForeignKey('Fraction', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    reputation = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'person_fraction'
        # app_label = 'poll'

    def __str__(self):
        return "%s, %s" % (self.person, self.fraction)

    def get_absolute_url(self):
        return reverse('poll:person-fraction-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class PersonLocation(models.Model):
    """
    person - персонаж
    location -  локация
    reputation - поправка на репутацию персонажа в текущей локации
    Для подсчета репутации персонажа. Только одна запись. Все предыдущие уходят в History
    """
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', related_name='current_location',
                                 verbose_name="Текущая Локация", on_delete=models.CASCADE)
    reputation = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'person_location'
        # app_label = 'poll'

    def __str__(self):
        return "%s, %s" % (self.person, self.location)

    def get_absolute_url(self):
        return reverse('poll:person-location-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class PersonRegion(models.Model):
    """
    person - персонаж
    region -  Регион
    district - Дистрикт
    Регион м Дмстрикт Определяются по координатам их центров (квадрата и шестиугольника).
    Это текущее местоположение в терминах регионов и терминах дистриктов.
    Нумерация регионов сквозная по всей карте.
    Нумерация дистриктов сквозная внутри регионов
    Только одна запись для каждого Персонажа. Все предыдущие записи уходят в History
    """
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    region = models.ForeignKey('Region', related_name='current_region',
                               verbose_name="Текущий Регион", on_delete=models.CASCADE)
    district = models.ForeignKey('District', related_name='current_district',
                                 verbose_name="Текущий Дистрикт", on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'person_region'
        # app_label = 'poll'

    def __str__(self):
        return "%s, %s, %s" % (self.person, self.region, self.district)

    def get_absolute_url(self):
        return reverse('poll:person-region-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class PersonBar(models.Model):
    """ слепок состояния персонажа в моменты времени"""
    person = models.ForeignKey('Person', on_delete=models.CASCADE, blank=True, null=True)
    race = models.ForeignKey('Race', on_delete=models.CASCADE, blank=True, null=True)
    summary_points = models.JSONField(verbose_name='Суммарные очки характеристик', blank=True, null=True)
    summary_permissions = models.JSONField(verbose_name='Суммарные очки умений', blank=True, null=True)
    summary_resistances = models.JSONField(verbose_name='Суммарные очки сопротивлений', blank=True, null=True)
    summary_equipment = models.JSONField(verbose_name='Суммарные слоты экипировки', blank=True, null=True)
    unallocated_points = models.IntegerField(verbose_name='Нераспределенные очки характеристик', default=0)
    unallocated_permissions = models.IntegerField(verbose_name='Нераспределенные очки умений', default=0)
    fov = models.IntegerField(verbose_name='Область обзора', default=0)
    rov = models.IntegerField(verbose_name='Дальность обзора', default=0)
    level = models.IntegerField(verbose_name='Уровень', default=0)
    conditions = models.JSONField(verbose_name='Кондиции', blank=True, null=True)

    def __str__(self):
        return "%s" % self.person.person_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('poll:person-bar-detail', kwargs={'pk': self.pk})

    class Meta:
        managed = True
        db_table = 'person_bar'


class ActionType(models.Model):
    """
    Возможные типы действий

    """
    action_type_name = models.CharField(verbose_name='Тип действия', max_length=100, blank=True, null=True)
    action_type_alias = models.CharField(verbose_name='Алиас типа', max_length=100, blank=True, null=True)
    action_type_description = RichTextField(verbose_name='Описание типа', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'action_type'
        verbose_name = "ActionType"
        verbose_name_plural = "ActionTypes"
        # app_label = 'poll'

    def __str__(self):
        return "%s" % self.action_type_name

    def get_absolute_url(self):
        return reverse('poll:action_type-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(ActionType, self).save(*args, **kwargs)


class Action(Info):
    """
    Перечень Действий с указанием прайсов на них
    """
    action_name = models.CharField(verbose_name='Название', max_length=100, blank=True, null=True)
    action_alias = models.CharField(verbose_name='Алиас', max_length=100, blank=True, null=True)
    action_description = RichTextField(verbose_name='Описание', blank=True, null=True)
    agg_points = None
    duration = models.IntegerField(verbose_name="Срок", default=0)
    action_type = models.ManyToManyField('ActionType')

    class Meta:
        managed = True
        db_table = 'action'
        verbose_name = "Action"
        verbose_name_plural = "Actions"
        # app_label = 'poll'

    def __str__(self):
        return "%s" % self.action_name

    def get_absolute_url(self):
        return reverse('poll:action-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):

        points = dict()
        for key in slovar.dict_points.keys():
            points[key] = self.__getattribute__(key)
        self.__setattr__("points", json.dumps(points, indent=4))

        permissions = dict()
        for key in slovar.dict_permissions.keys():
            permissions[key] = self.__getattribute__(key)
        self.__setattr__("permissions", json.dumps(points, indent=4))

        resistances = dict()
        for key in slovar.dict_resistances.keys():
            resistances[key] = self.__getattribute__(key)
        self.__setattr__("resistances", json.dumps(points, indent=4))

        equipment = dict()
        for key in slovar.dict_equipment.keys():
            equipment[key] = self.__getattribute__(key)
        self.__setattr__("equipment", json.dumps(points, indent=4))
        super(Action, self).save(*args, **kwargs)


class History(models.Model):
    """
    Журнал действий персонажей
    должен быть общий по всем действиям и персонажам.
    нужно сквозную нумерацию ходов каждого персонажа иметь
    """
    person = models.ForeignKey('Person', on_delete=models.CASCADE, blank=True, null=True)
    action = models.ForeignKey('Action', on_delete=models.CASCADE, blank=True, null=True)
    move_number_begin = models.IntegerField(verbose_name='Номер хода - начало действия Персонажа')
    move_number_end = models.IntegerField(verbose_name='Номер хода - конец действия Персонажа')
    action_type = models.ManyToManyField('ActionType', verbose_name='тип действия Персонажа')
    points_old = models.JSONField(verbose_name='Прежние очки характеристик', blank=True, null=True)
    points_new = models.JSONField(verbose_name='Новые очки характеристик', blank=True, null=True)
    permissions_old = models.JSONField(verbose_name='Прежние навыки', blank=True, null=True)
    permissions_new = models.JSONField(verbose_name='Новые навыки', blank=True, null=True)
    resistances_old = models.JSONField(verbose_name='Прежние сопротивления', blank=True, null=True)
    resistances_new = models.JSONField(verbose_name='Новые сопротивления', blank=True, null=True)
    equipment_old = models.JSONField(verbose_name='Прежнее снаряжение', blank=True, null=True)
    equipment_new = models.JSONField(verbose_name='Новое снаряжение', blank=True, null=True)
    un_points_old = models.IntegerField(verbose_name='Прежние нераспределенные очки', blank=True, null=True)
    un_points_new = models.IntegerField(verbose_name='Новые нераспределенные очки', blank=True, null=True)
    un_permissions_old = models.IntegerField(verbose_name='Прежние нераспределенные навыки', blank=True, null=True)
    un_permissions_new = models.IntegerField(verbose_name='Новые нераспределенные навыки', blank=True, null=True)
    fov_old = models.IntegerField(verbose_name='Прежняя область обзора', blank=True, null=True)
    fov_new = models.IntegerField(verbose_name='Новая область обзора', blank=True, null=True)
    rov_old = models.IntegerField(verbose_name='Прежняя дальность обзора', blank=True, null=True)
    rov_new = models.IntegerField(verbose_name='Новая дальность обзора', blank=True, null=True)
    level_old = models.IntegerField(verbose_name='Прежний уровень', blank=True, null=True)
    level_new = models.IntegerField(verbose_name='Новый уровень', blank=True, null=True)
    last_update = models.TimeField(auto_now=True)
    conditions_old = models.JSONField(verbose_name='Прежние кондиции', blank=True, null=True)
    conditions_new = models.JSONField(verbose_name='Новые кондиции', blank=True, null=True)
    location_old = models.ForeignKey('Location', related_name="location_old", verbose_name='Прежняя локация',
                                     on_delete=models.CASCADE, blank=True, null=True)
    location_new = models.ForeignKey('Location', related_name="location_new", verbose_name='Новая локация',
                                     on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'history'
        verbose_name = "History"

        # app_label = 'poll'

    def __str__(self):
        return "%s, %s, %s" % (self.person, self.action, self.last_update)

    def get_absolute_url(self):
        return reverse('poll:history-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(History, self).save(*args, **kwargs)


class Money(models.Model):
    """
    Заклинания
    """

    class MoneyType(models.TextChoices):
        COPPER = '0', 'Медь',
        SILVER = '1', 'Серебро',
        GOLD = '2', 'Золото',
        OTHER = '3', 'Прочее'

    def is_upperclass(self):
        return self.money_type in {
            self.MoneyType.COPPER,
            self.MoneyType.SILVER,
            self.MoneyType.GOLD,
            self.MoneyType.OTHER
        }

    money_type = models.CharField(
        verbose_name='Название',
        max_length=1,
        choices=MoneyType.choices,
        default=MoneyType.COPPER)
    weight = models.IntegerField(verbose_name='Вес', default=1)
    rate = models.IntegerField(verbose_name='Номинал', default=1)

    class Meta:
        managed = True
        db_table = 'money'
        verbose_name = "Money"
        verbose_name_plural = "Money"
        # app_label = 'poll'

    def __str__(self):
        return "%s, %s, %s" % (self.get_money_type_display(), self.weight, self.rate)

    def get_absolute_url(self):
        return reverse('poll:money-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Money, self).save(*args, **kwargs)


class Inventory(models.Model):
    """
      Инвентарь (рюкзак)
      """
    inventory_name = models.CharField(verbose_name='Название', max_length=128, blank=True, null=True)
    inventory_description = RichTextField(verbose_name='Описание', blank=True, null=True)
    person = models.ForeignKey('Person', on_delete=models.CASCADE, verbose_name='Персонаж')
    inventory_max_weight = models.IntegerField(verbose_name='Максимальный вес', default=0)
    consumables = models.ManyToManyField(Consumable, verbose_name='Расходники')
    things = models.ManyToManyField(Thing, verbose_name='Артефакты')
    money = models.ManyToManyField(Money, verbose_name='Ценности')

    class Meta:
        managed = True
        db_table = 'inventory'
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"
        # app_label = 'poll'

    def __str__(self):
        return "%s" % self.inventory_name

    def get_absolute_url(self):
        return reverse('poll:inventory-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Inventory, self).save(*args, **kwargs)

    # @property
    # def get_inventory_stat(self):
    #     inventory_things = self.things.all()
    #     inventory_consumables = self.consumables.all()
    #     inventory_money = self.money.all()
    #     inventory_things_sum_weight, inventory_things_sum_value = inventory_things.aggregate(Sum('weight'), Sum('sale_price'))
    #     inventory_consumables_sum_weight, inventory_consumables_sum_value = inventory_consumables.aggregate(Sum('weight'),
    #                                                                                          Sum('sale_price'))
    #     inventory_money_sum_weight, inventory_money_sum_value = inventory_money.aggregate(Sum('weight'), Sum('rate'))
    #     inventory_sum_weight = inventory_things_sum_weight + inventory_consumables_sum_weight + inventory_money_sum_weight
    #     inventory_sum_value = inventory_things_sum_value + inventory_consumables_sum_value + inventory_money_sum_value
    #     inventory_stat = dict(inventory_things_sum_weight=inventory_things_sum_weight,
    #                           inventory_things_sum_value=inventory_things_sum_value,
    #                           inventory_consumables_sum_weight=inventory_consumables_sum_weight,
    #                           inventory_consumables_sum_value=inventory_consumables_sum_value,
    #                           inventory_money_sum_weight=inventory_money_sum_weight,
    #                           inventory_money_sum_value=inventory_money_sum_value, inventory_sum_weight=inventory_sum_weight,
    #                           inventory_sum_value=inventory_sum_value)
    #     return "%s" % self.inventory_stat


class Safe(models.Model):
    """
      Сейф
      """
    safe_name = models.CharField(verbose_name='Название', max_length=128, blank=True, null=True)
    safe_description = RichTextField(verbose_name='Описание', blank=True, null=True)
    person = models.ForeignKey('Person', on_delete=models.CASCADE, verbose_name='Персонаж')
    rental_price = models.IntegerField(verbose_name='Стоимость аренды', default=0)
    max_value = models.IntegerField(verbose_name='Максимальная стоимость', default=0)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, verbose_name='Локация')
    consumables = models.ManyToManyField(Consumable, verbose_name='Расходники')
    things = models.ManyToManyField(Thing,  verbose_name='Артефакты')
    money = models.ManyToManyField(Money,  verbose_name='Ценности')

    class Meta:
        managed = True
        db_table = 'safe'
        verbose_name = "Safe"
        verbose_name_plural = "Safes"
        # app_label = 'poll'

    @property
    def safe_name_default(self):
        self.safe_name = self.person.person_name+"'s Safe"
        return "%s" % self.safe_name

    # @property
    # def get_safe_stat(self):
    #     safe_things = self.things.all()
    #     safe_consumables = self.consumables.all()
    #     safe_money = self.money.all()
    #     safe_things_sum_weight, safe_things_sum_value = safe_things.aggregate(Sum('weight'), Sum('sale_price'))
    #     safe_consumables_sum_weight, safe_consumables_sum_value = safe_consumables.aggregate(Sum('weight'),
    #                                                                                          Sum('sale_price'))
    #     safe_money_sum_weight, safe_money_sum_value = safe_money.aggregate(Sum('weight'), Sum('rate'))
    #     safe_sum_weight = safe_things_sum_weight + safe_consumables_sum_weight + safe_money_sum_weight
    #     safe_sum_value = safe_things_sum_value + safe_consumables_sum_value + safe_money_sum_value
    #     inventory_stat = dict(safe_things_sum_weight=safe_things_sum_weight,
    #                           safe_things_sum_value=safe_things_sum_value,
    #                           safe_consumables_sum_weight=safe_consumables_sum_weight,
    #                           safe_consumables_sum_value=safe_consumables_sum_value,
    #                           safe_money_sum_weight=safe_money_sum_weight,
    #                           safe_money_sum_value=safe_money_sum_value, safe_sum_weight=safe_sum_weight,
    #                           safe_sum_value=safe_sum_value)
    #     return self.safe_stat

    def __str__(self):
        return "%s" % self.safe_name

    def get_absolute_url(self):
        return reverse('poll:safe-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Safe, self).save(*args, **kwargs)


class Spell(models.Model):
    """
    Заклинания
    """
    spell_name = models.CharField(verbose_name='Название', max_length=128, blank=True, null=True)
    spell_description = RichTextField(verbose_name='Описание', blank=True, null=True)
    permissions_to_use = models.JSONField(verbose_name='очки навыков для применения', blank=True, null=True)
    points_from_use = models.JSONField(verbose_name='очки характеристик от применения', blank=True, null=True)
    permissions_from_use = models.JSONField(verbose_name='очки навыков от применения', blank=True, null=True)
    resistances_from_use = models.JSONField(verbose_name='очки сопротивлений от применения', blank=True, null=True)
    conditions_from_use = models.JSONField(verbose_name='Прирост кондиций', blank=True, null=True)
    equipment_from_use = models.JSONField(verbose_name='расширение слотов от применения', blank=True, null=True)
    damage_from_use = models.JSONField(verbose_name='очки урона противнику от применения', blank=True, null=True)
    thing_list = models.JSONField(verbose_name='Список Артефактов для использования', blank=True, null=True)
    consumable_list = models.JSONField(verbose_name='Список Расходников для использования', blank=True, null=True)
    person = models.ManyToManyField(Person,  verbose_name='Персонаж')
    thing = models.ManyToManyField(Thing, verbose_name='Артефакты')
    consumable = models.ManyToManyField(Consumable, verbose_name='Расходники')

    class Meta:
        managed = True
        db_table = 'spell'
        verbose_name = "Spell"
        verbose_name_plural = "Spells"
        # app_label = 'poll'

    def __str__(self):
        return "%s" % self.spell_name

    def get_absolute_url(self):
        return reverse('poll:spell-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Spell, self).save(*args, **kwargs)


