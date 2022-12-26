import shutil
import tempfile
from unittest import TestCase
from django.db.models import TextChoices
from ..models import Owner, Race, Person
from mysite import settings
import sys
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.mysite.settings")


class Settings(TestCase):
    @classmethod
    def SetupClass(cls):
        super().setUpClass()

        # создаем временную папку для медиафайлов
        # на момент теста она будет переопределена
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

        # БД Создаем тестовую запись Owner
        cls.owner = Owner.objects.create(
            owner_name='Test',
            owner_description='Test_description',
            link='test_link',
            owner_status='1',
            owner_img=tempfile.NamedTemporaryFile(suffix=".png").name,
        )

        class Races(TextChoices):
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
                self.other
            }

        # # БД Создаем тестовую запись Race
        cls.race = Race.objects.create(
            race_name=Races.ELF.name,
            race_description='test_race_description',
            race_img=tempfile.NamedTemporaryFile(suffix=".png").name,
            lifetime='100',
            start_points='{"AP_START": 1, "BP_START": 5, "CP_START": 0, "FP_START": 2, "IP_START": 2, "LP_START": 0, "MP_START": 2, "PP_START": 1, "SP_START": 1}',
            finish_points='{"AP_MAX": 10, "BP_MAX": 40, "CP_MAX": 5, "FP_MAX": 20, "IP_MAX": 15, "LP_MAX": 0, "MP_MAX": 10, "PP_MAX": 10, "SP_MAX": 10}',
            start_resistances='{"cut_res_start": 0, "dirt_res_start": 20, "fire_res_start": -25, "holy_res_start": 30, "stab_res_start": 15, "wind_res_start": 10, "crush_res_start": 5, "curse_res_start": -40, "water_res_start": 20, "lightning_res_start": 15}',
            start_permissions='{"Dirt_access_start": -1, "Fire_access_start": -3, "Holy_access_start": -1, "Wind_access_start": -1, "Bleed_access_start": -3, "Curse_access_start": -11, "Water_access_start": -1, "Mental_access_start": -2, "Nature_access_start": -1, "Cutting_access_start": -1, "Polearm_access_start": -3, "Shields_access_start": -1, "Crushing_access_start": 0, "Stabbing_access_start": -1, "Lightning_access_start": -2, "Onehanded_access_start": -2, "Twohanded_access_start": -3, "Small_arms_access_start": -3}',
            equipment='{"ITEM_SLOT_START": 2, "CHEST_STATUS_START": 1, "SHOES_STATUS_START": 2, "GLOVES_STATUS_START": 2, "HELMET_STATUS_START": 1}',
            fov=0,
            rov=0

        )

        obj = Race.objects.create(race_name='1')
        assert obj.race_name == obj.Races.ELF == '1'
        assert Race.Races(obj.race_name) is obj.Races.ELF
        assert Race.Races(obj.race_name).value == '1'
        assert Race.Races(obj.race_name).label == 'Эльф'
        assert Race.Races(obj.race_name).name == 'ELF'
        assert Race.objects.filter(month=Race.Races.ELF).count() >= 1

        obj2 = Race(race_name=Race.Races.ANGEL)
        assert obj2.get_race_name_display() == obj2.Races(obj2.race_name).label

        # БД создаем тестовую запись Person
        cls.person = Person.object.create(
            person_name='Test_Person',
            person_img=tempfile.NamedTemporaryFile(suffix=".png").name,
            owner=cls.owner,
            link='Test_person_link',
            biography='test_biography',
            character='test_character',
            interests='test_interests',
            phobias='test_phobias',
            race=cls.race,
            location_birth=1,
            birth_date='22.10.2022',
            location_death=1,
            death_date='22.10.2022',
            status=1
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True
                      )
class OwnerModelTest(Settings):
    # проверяем, что объект с заданным именем был создан

    def test_create_owner(cls):
        owner = Owner.objects.get(id=cls.owner.id)
        expected_object_name = f'{owner.owner_name}'
        cls.assertEqual(expected_object_name, 'Test')

    # проверяем, что страница по нужному адресу
    def test_get_absolute_url(cls):
        owner = Owner.objects.get(id=cls.owner.id)
        expected_url = '/owners/' + str(cls.owner.id)+'/'
        # This will also fail if the urlconf is not defined.
        cls.assertEquals(owner.get_absolute_url(), expected_url)
