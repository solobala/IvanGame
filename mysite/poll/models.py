from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

# Create your models here.


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
    link = models.CharField('Ссылка', max_length=9, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    owner_status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.WITHOUT,)
    owner_img = models.ImageField('Изображениеэ', upload_to='media/euploads')

    def __str__(self):
        # return self
        # return "%s, %s, %s, %s" % (self.owner_name, self.owner_description, self.link, self.owner_status)
        return "%s" % self.owner_name

    def get_absolute_url(self):
        # return reverse('poll:owner_detail', args=[str(self.id)])
        return reverse('poll:owner-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        # возвращает объект Owner с добавленным owner_status

        try:
            if self.filter(person__status=1).count() == 0:
                self.owner_status = self.Status.BUSY
            else:
                self.owner_status = self.Status.FREE
        except:
            self.owner_status = self.Status.FREE
        finally:
            super().save(*args, **kwargs)

    @property
    def full_name(self):
        """Возвращает имя игрока"""
        return "%s" % self.owner_name

    class Meta:
        managed = True
        db_table = 'owner'
        verbose_name = "Owner"
        verbose_name_plural = "Owners"
        # app_label = 'poll'
        permissions = [
            ('special_status', 'Can edit all owners'),
        ]


class Race(models.Model):
    """
    Класс Раса  Персонажа (Person).
  `race_name` varchar(45) NOT NULL COMMENT 'Наименование расы персонажа',
  `race_description` varchar(200) DEFAULT NULL COMMENT 'Описание возможностей расы персонажа',
  `start_points` json DEFAULT NULL COMMENT 'стартовые  значение очков стамины, маны, интелекта, силы, ловкости, веры,
  удачи, харизмы и рассудка в формате JSON',
  `finish_points` json DEFAULT NULL COMMENT 'финишные значение очков стамины, маны, интелекта, силы, ловкости, веры,
  удачи, харизмы и рассудка в формате JSON',
  `start_resistanses` json DEFAULT NULL COMMENT 'стартовые значение устойчивости к воздействию водой, огнем, ветром ,
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
        OTHER ='23', 'прочие'

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
            self.other
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
            self.get_race_name_display())

    def save(self, *args, **kwargs):
        # keys = ["SP_START", "MP_START", "IP_START", "PP_START", "AP_START", "FP_START", "LP_START", "CP_START",
        #         "BP_START"]
        # labels = 'Стамина, Колдовство, Интеллект, Сила, Ловкость, Вера, Удача, Харизма, Рассудок'
        # my_dict = dict(zip(keys, labels.split(', ')))
        # sp = dict()
        # for key in keys:
        #     value = json.loads(self.start_points).get(key)
        #     sp[my_dict.get(key)] = 1
        # self.start_points = json.dumps(sp)
        #
        # keys = ["SP_MAX", "MP_MAX", "IP_MAX", "PP_MAX", "AP_MAX", "FP_MAX", "LP_MAX", "CP_MAX",
        #         "BP_MAX"]
        # fp = dict()
        # my_dict = dict(zip(keys, labels.split(', ')))
        # for key in keys:
        #     fp[my_dict.get(key)] = json.loads(self.finish_points).get(key)
        # self.finish_points = json.dumps(fp)
        #
        # sr = dict()
        # keys = ["fire_res_start", "water_res_start", "wind_res_start", "dirt_res_start", "lightning_res_start",
        #         "curse_res_start", "crush_res_start", "cut_res_start", "stab_res_start"]
        # labels = 'Огонь, Вода, Воздух, Земля, Молнии, Свет, Тьма, Дробление, Порезы, Протыкание'
        #
        # my_dict = dict(zip(keys, labels.split(', ')))
        # for key in keys:
        #     sr[my_dict.get(key)] = json.loads(self.start_resistanses).get(key)
        # self.start_resistanses = json.dumps(sr)
        #
        # stp = dict()
        # keys = ["Fire_access_start", "Water_access_start", "Wind_access_start", "Dirt_access_start",
        #         "Lightning_access_start", "Holy_access_start", "Curse_access_start", "Bleed_access_start",
        #         "Nature_access_start", "Mental_access_start", "Twohanded_access_start", "Polearm_access_start",
        #         "Onehanded_access_start", "Stabbing_access_start", "Cutting_access_start", "Crushing_access_start",
        #         "Small_arms_access_start", "Shields_access_start"]
        # labels = 'Пирокинектика, Гидрософистика, Аэрософистика, Геомантия, Киловактика, Элафристика, Катифристика,\
        #        Гематомантия, Ботаника, Психистика, Владение навыками Двуручного оружия, Владение навыками
        #        Древкового оружия,\
        #        Владение навыками Одноручного оружия, Владение навыками Колющего оружия, Владение навыками
        #        Режущего оружия,\
        #        Владение навыками Дробящего оружия, Владение навыками Стрелкового оружия, Владение навыками
        #        Стрелкового оружия'
        # my_dict = dict(zip(keys, labels.split(', ')))
        # for key in keys:
        #     stp[my_dict.get(key)] = json.loads(self.start_permissions).get(key)
        # self.start_permissions = json.dumps(stp)
        #
        # eq = dict()
        # keys = []
        # labels = 'Шлем, Нагрудник, Сапоги, Наручи, Прочее'
        # my_dict = dict(zip(keys, labels.split(', ')))
        # for key in keys:
        #     eq[my_dict.get(key)] = json.loads(self.equipment).get(key)
        # self.equipment = json.dumps(eq)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        #  return reverse('poll:owner_detail', args=[str(self.id)])
        return reverse('poll:race-detail', kwargs={'pk': self.pk})

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

    person_name = models.CharField(max_length=45, blank=True, null=True)
    person_img = models.ImageField(default='media/euploads/python.png')
    owner = models.ForeignKey('Owner', on_delete=models.CASCADE, blank=True, null=True)
    link = models.CharField(max_length=30, blank=True, null=True)
    biography = RichTextField(blank=True, null=True)
    character = RichTextField(blank=True, null=True)
    interests = RichTextField(blank=True, null=True)
    phobias = RichTextField(blank=True, null=True)
    race = models.ForeignKey(Race, on_delete=models.CASCADE, null=True)
    location_birth = models.IntegerField(blank=True, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    location_death = models.IntegerField(blank=True, null=True)
    death_date = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=Status.choices, default=Status.FREE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # free = FreePersonManager()
    # busy = BusyPersonManager()
    # freezed = FreezedPersonManager()

    def __str__(self):
        return self.person_name

    def get_absolute_url(self):
        #  return reverse('poll:person_detail', args=[str(self.id)])
        return reverse('poll:person-detail', kwargs={'pk': self.pk})


    class Meta:
        managed = True
        db_table = 'person'
        verbose_name = "Person"
        verbose_name_plural = "Persons"
        permissions = [
            ('special_status', 'Can list all persons'),
        ]
        # app_label = 'poll'


class Zone(models.Model):
    zone_name = models.CharField(max_length=128, blank=True, null=True)
    zone_description = RichTextUploadingField(verbose_name='Описание', blank=True, null=True)

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
    location_name = models.CharField(max_length=128, blank=True, null=True)
    location_description = RichTextUploadingField(verbose_name='Описание', blank=True, null=True)
    zone = models.ForeignKey(Zone, on_delete=models.DO_NOTHING)

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
    region_name = models.CharField(max_length=128, blank=True, null=True)
    region_description = RichTextUploadingField(verbose_name='Описание', blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    x = models.IntegerField(blank=True, null=True)
    y = models.IntegerField(blank=True, null=True)

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
        return "%s" % self.distrtict_name

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
        self.group_name = self.members.through.objects.filter(group__id=self.id)[0].inviter.person_name
        try:
            if self.members.count() >= 1:
                for member in self.members.through.objects.filter(group__id=self.id):
                    self.group_name = self.group_name + '; ' + member.person.person_name

        except:
            pass
        finally:
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
            if self.members.count() >= 1:
                self.group_name = self.members.through.objects.filter(
                    group__id=self.pk).inviter.person_name
                for member in self.members.through.objects.filter(group__id=self.pk):
                    self.group_name = self.group_name + '; ' + member.person.person_name
        except:
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
    fraction_name = models.CharField(max_length=128, blank=True, null=True)
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

    reputation - репутация персонажа в текущей локации
    """
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)

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


class Info(models.Model):
    agg_points = models.IntegerField(verbose_name='Характеристики', default=0)
    points = models.JSONField(verbose_name='Характеристики', blank=True, null=True)
    SP = models.IntegerField(verbose_name="Стамина", default=0)
    MP = models.IntegerField(verbose_name="Колдовство", default=0)
    IP = models.IntegerField(verbose_name="Интеллект", default=0)
    PP = models.IntegerField(verbose_name="Сила", default=0)
    AP = models.IntegerField(verbose_name="Ловкость", default=0)
    FP = models.IntegerField(verbose_name="Вера", default=0)
    LP = models.IntegerField(verbose_name="Удача", default=0)
    CP = models.IntegerField(verbose_name="Харизма", default=0)
    BP = models.IntegerField(verbose_name="Рассудок", default=0)

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
    Fire_access = models.IntegerField(verbose_name="Пирокинектика", default=0)
    Water_access = models.IntegerField(verbose_name="Гидрософистика", default=0)
    Wind_access = models.IntegerField(verbose_name="Аэрософистика", default=0)
    Dirt_access = models.IntegerField(verbose_name="Геомантия", default=0)
    Lightning_access = models.IntegerField(verbose_name="Киловактика", default=0)
    Holy_access = models.IntegerField(verbose_name="Элафристика", default=0)
    Curse_access = models.IntegerField(verbose_name="Катифристика", default=0)
    Bleed_access = models.IntegerField(verbose_name="Гематомантия", default=0)
    Nature_access = models.IntegerField(verbose_name="Ботаника", default=0)
    Mental_access = models.IntegerField(verbose_name="Псифистика", default=0)
    Twohanded_access = models.IntegerField(verbose_name="Двуручное оружие", default=0)
    Polearm_access = models.IntegerField(verbose_name="Древковое оружие", default=0)
    Onehanded_access = models.IntegerField(verbose_name="Одноручное оружие", default=0)
    Stabbing_access = models.IntegerField(verbose_name="Колющее оружие", default=0)
    Cutting_access = models.IntegerField(verbose_name="Режущее оружие", default=0)
    Crushing_access = models.IntegerField(verbose_name="Дробящее оружие", default=0)
    Small_arms_access = models.IntegerField(verbose_name="Стрелковое оружие", default=0)
    Shields_access = models.IntegerField(verbose_name="Щиты", default=0)

    equipment = models.JSONField(verbose_name='Снаряжение', blank=True, null=True)
    helmet_status = models.IntegerField(verbose_name='Шлем', default=0)
    chest_status = models.IntegerField(verbose_name='Нагрудник', default=0)
    shoes_status = models.IntegerField(verbose_name='Сапоги', default=0)
    gloves_status = models.IntegerField(verbose_name='Наручи', default=0)
    item_status = models.IntegerField(verbose_name='Прочее', default=0)

    fov = models.IntegerField(verbose_name='Область обзора', default=0)
    rov = models.IntegerField(verbose_name='Дальность обзора', default=0)

    class Meta:
        abstract = True


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

    def __str__(self):
        return "%s" % self.person.person_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('poll:person-bar-detail', kwargs={'pk': self.pk})

    class Meta:
        managed = True
        db_table = 'person_bar'


class Action(Info):

    action_name = models.CharField(verbose_name='Название',max_length=100, blank=True, null=True)
    action_alias = models.CharField(verbose_name='Алиас', max_length=100, blank=True, null=True)
    action_description = RichTextField(verbose_name='Описание', blank=True, null=True)
    agg_points = None

    class Meta:
        managed = True
        db_table = 'action'
        verbose_name = "Action"
        verbose_name_plural = "Actions"
        # app_label = 'poll'

    def __str__(self):
        return "%s, %s" % (self.action_name, self.action_alias)

    def get_absolute_url(self):
        return reverse('poll:action-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Action, self).save(*args, **kwargs)


class Feature(Info):

    feature_name = models.CharField(max_length=128, blank=True, null=True)
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
        super(Feature, self).save(*args, **kwargs)
