import json

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


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

    owner_name = models.CharField(max_length=45, blank=True, null=True)
    owner_description = models.CharField(max_length=200, blank=True, null=True)
    link = models.CharField(max_length=9, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    owner_status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.WITHOUT,
    )

    def __str__(self):
        # return self

        #return "%s, %s, %s, %s" % (self.owner_name, self.owner_description, self.link, self.owner_status)
        return "%s" % (self.owner_name)

    def get_absolute_url(self):
        #  return reverse('poll:owner_detail', args=[str(self.id)])
        return reverse('poll:owner-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        # возвращает объект Owner с добавленным owmer_status

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
        return "%s" % (self.owner_name)

    class Meta:
        managed = True
        db_table = 'owner'
        # app_label = 'poll'


class Race(models.Model):
    """
    Класс Раса  Персонажа (Person).

  `race_name` varchar(45) NOT NULL COMMENT 'Наименование расы персонажа',
  `race_description` varchar(200) DEFAULT NULL COMMENT 'Описание возможностей расы персонажа',
  `start_points` json DEFAULT NULL COMMENT 'стартовые  значение очков стамины, маны, интелекта, силы, ловкости, веры, удачи, харизмы и рассудка в формате JSON',
  `finish_points` json DEFAULT NULL COMMENT 'финишные значение очков стамины, маны, интелекта, силы, ловкости, веры, удачи, харизмы и рассудка в формате JSON',
  `start_resistanses` json DEFAULT NULL COMMENT 'стартовые значение устойчивости к воздействию водой, огнем, ветром и т.д',
  `start_permissions` json DEFAULT NULL COMMENT 'стартовые значение разрешений на воздействие водой, огнем, ветром и т.д',
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
        ORK = '22', 'Орк'

    def is_upperclass(self):
        return self.race in {
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
        }

    race_name = models.CharField(max_length=20, choices=Races.choices, default=Races.HUMAN)
    race_description = models.TextField(verbose_name='Описание', blank=True, null=True)
    lifetime = models.IntegerField(verbose_name='Продолжительность жизни', default=100)
    start_points = models.JSONField(verbose_name='Стартовые очки характеристик')
    finish_points = models.JSONField(verbose_name='Предельные очки характеристик')
    start_resistanses = models.JSONField(verbose_name='Стартовые очки сопротивлений')
    start_permissions = models.JSONField(verbose_name='Стартовые очки навыков')
    equipment = models.JSONField(verbose_name='Снаряжение')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):

        # return "%s, %s, %s, %s, %s, %s, %s, %s" % (
        #     self.get_race_name_display(), self.race_description, self.lifetime, self.start_points,
        #     self.finish_points, self.start_resistanses, self.start_permissions, self.equipment)
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
        #        Гематомантия, Ботаника, Психистика, Владение навыками Двуручного оружия, Владение навыками Древкового оружия,\
        #        Владение навыками Одноручного оружия, Владение навыками Колющего оружия, Владение навыками Режущего оружия,\
        #        Владение навыками Дробящего оружия, Владение навыками Стрелкового оружия, Владение навыками Стрелкового оружия'
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

    person_name = models.CharField(max_length=45)
    owner = models.ForeignKey('Owner', on_delete=models.CASCADE)
    link = models.CharField(max_length=30, blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    character = models.TextField(blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    phobias = models.TextField(blank=True, null=True)
    race = models.ForeignKey(Race, on_delete=models.CASCADE, null=True)
    location_birth = models.IntegerField(blank=True, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    location_death = models.IntegerField(blank=True, null=True)
    death_date = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=Status.choices, default=Status.FREE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.person_name
        # return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.person_name, self.owner, self.link,
        #                                                            self.biography, self.character, self.interests,
        #                                                            self.phobias, self.race, self.location_birth,
        #                                                            self.birth_date,
        #                                                            self.death_date, self.status, ', '.join(
        #     membership.person for membership in self.membership.all()))

    def get_absolute_url(self):
        #  return reverse('poll:person_detail', args=[str(self.id)])
        return reverse('poll:person-detail', kwargs={'pk': self.pk})

    @property
    def full_name(self):
        """Возвращает имя Персонажа"""
        return "%s" % (self.person_name)

    class Meta:
        managed = True
        db_table = 'person'
        # app_label = 'poll'


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
        # return self.group_name, self_members
        self.group_name = self.members.through.objects.filter(
            group__id=self.id)[0].inviter.person_name
        try:
            if self.members.count() >= 1:
                for member in self.members.through.objects.filter(group__id=self.id):
                    self.group_name = self.group_name + '; ' + member.person.person_name

        except:
            pass
        finally:
            return "%s" % (self.group_name)

    def get_absolute_url(self):
        #  return reverse('poll:person_detail', args=[str(self.id)])
        return reverse('poll:group-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        # возвращает объект Group с измененным group_name
        # mo.Group.objects.get(id=7).members.through.objects.filter(group__id=7) - возщвращает набор membership из пар inviter-person
        # Можно получить список группы либо по person, либо по inviter либо по названию группы
        # ПОиск участников группы по  invitor -  mo.Group.objects.get(id=2).members.through.objects.filter(person_id=mo.Person.objects.get(person_name='Лилит Игнис').id)
        # ПОиск участников группы по  person -  mo.Group.objects.get(id=2).members.through.objects.filter(inviter_id=mo.Person.objects.get(person_name='Люцифер Вераз').id)
        try:
            if self.members.count() >= 1:
                self.group_name = self.members.through.objects.filter(
                    group__id=self.id).inviter.person_name
                for member in self.members.through.objects.filter(group__id=self.id):
                    self.group_name = self.group_name + '; ' + member.person.person_name
        except:
            pass
        finally:
            super().save(*args, **kwargs)


class Location(models.Model):
    location_name = models.CharField(max_length=128, blank=True, null=True)
    location_description = models.TextField(verbose_name='Описание', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'location'
        # app_label = 'poll'

    def __str__(self):
        return "%s" % (self.location_name)

    def get_absolute_url(self):

        return reverse('poll:location-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Fraction(models.Model):
    fraction_name = models.CharField(max_length=128, blank=True, null=True)
    fraction_description = models.TextField(verbose_name='Описание', blank=True, null=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'fraction'
        # app_label = 'poll'

    def __str__(self):
        return "%s" % (self.fraction_name)

    def get_absolute_url(self):
        return reverse('poll:fraction-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Clan(models.Model):
    clan_name = models.CharField(max_length=128, blank=True, null=True)
    clan_description = models.TextField(verbose_name='Описание', blank=True, null=True)
    chief = models.ForeignKey('Person', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'clan'
        # app_label = 'poll'

    def __str__(self):
        return "%s" % (self.fraction_name)

    def get_absolute_url(self):
        return reverse('poll:fraction-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class FractionLocation(models.Model):
    """
    Репутация фракций в чужих локациях
    other_location - чужая локация
    reputation - репутация фракции в чужой локации
    """
    fraction = models.ForeignKey('Fraction', on_delete=models.CASCADE)

    other_location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name="other_location")
    reputation = location_death = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'fraction_location'
        # app_label = 'poll'

    def __str__(self):
        return "%s, %s, %s" % (self.fraction,  self.other_location)

    def get_absolute_url(self):
        return reverse('poll:fraction-location-detail', kwargs={'pk': self.pk})

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
    reputation = location_death = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'fraction_location'
        # app_label = 'poll'

    def __str__(self):
        return "%s, %s, %s" % (self.fraction, self.location, self.other_fraction)

    def get_absolute_url(self):
        return reverse('poll:fraction-location-detail', kwargs={'pk': self.pk})

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
        # app_label = 'poll'

    def __str__(self):
        return "%s" % (self.quest_name)

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
        # app_label = 'poll'

    def __str__(self):
        return "%s" % (self.party_name, self.quest)

    def get_absolute_url(self):
        return reverse('poll:party-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
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


class Bar(models.Model):
    """ слепок состояния персонажа в моменты времени"""

