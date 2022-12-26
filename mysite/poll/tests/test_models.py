import tempfile

from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import SimpleTestCase
from django.db.models import TextChoices
from ..models import Owner, Person, Race
from ..forms import NewUserForm
from django.urls import reverse, resolve
from ..views import index


# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.mysite.settings")


# Create your tests here.


#  Тест на добавление новых пользователей игры
class CustomUserTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='will',
            email='will@email.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'will')
        self.assertEqual(user.email, 'will@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='superadmin',
            email='solobala@yandex.ru',
            password='2305623056'
        )
        self.assertEqual(admin_user.username, 'superadmin')
        self.assertEqual(admin_user.email, 'solobala@yandex.ru')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


# Тесты на модель и views для Race
class RaceModelTest(TestCase):
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

    @classmethod
    def setUp(cls):
        # БД Создаем тестовую запись Race

        cls.race = Race.objects.create(
                race_name=cls.Races.ELF,
                race_description='test_race_description',
                race_img=tempfile.NamedTemporaryFile(suffix=".png").name,
                lifetime='100',
                start_points='{"AP_START": 1, "BP_START": 5, "CP_START": 0, "FP_START": 2, "IP_START": 2, '
                             '"LP_START": 0, "MP_START": 2, "PP_START": 1, "SP_START": 1}',
                finish_points='{"AP_MAX": 10, "BP_MAX": 40, "CP_MAX": 5, "FP_MAX": 20, "IP_MAX": 15, "LP_MAX": 0, '
                              '"MP_MAX": 10, "PP_MAX": 10, "SP_MAX": 10}',
                start_resistances='{"cut_res_start": 0, "dirt_res_start": 20, "fire_res_start": -25, '
                                  '"holy_res_start": 30, "stab_res_start": 15, "wind_res_start": 10, '
                                  '"crush_res_start": 5, "curse_res_start": -40, "water_res_start": 20, '
                                  '"lightning_res_start": 15}',
                start_permissions='{"Dirt_access_start": -1, "Fire_access_start": -3, "Holy_access_start": -1, '
                                  '"Wind_access_start": -1, "Bleed_access_start": -3, "Curse_access_start": -11, '
                                  '"Water_access_start": -1, "Mental_access_start": -2, "Nature_access_start": -1, '
                                  '"Cutting_access_start": -1, "Polearm_access_start": -3, "Shields_access_start": -1, '
                                  '"Crushing_access_start": 0, "Stabbing_access_start": -1, '
                                  '"Lightning_access_start": -2, "Onehanded_access_start": -2, '
                                  '"Twohanded_access_start": -3, "Small_arms_access_start": -3}',
                equipment='{"ITEM_SLOT_START": 2, "CHEST_STATUS_START": 1, "SHOES_STATUS_START": 2, '
                          '"GLOVES_STATUS_START": 2, "HELMET_STATUS_START": 1}',
                fov=0,
                rov=0
            )
        print('----races-----------')
        print(dir(cls.race))

    # проверяем, что объект с заданным именем был создан
    def test_create_race(self):
        race = Race.objects.get(id=self.race.id)
        expected_object_name = f'{race.race_name}'
        self.assertEqual(expected_object_name, '0')

        assert race.race_name == race.Races.ELF == '0'
        assert Race.Races(race.race_name) is race.Races.ELF
        assert Race.Races(race.race_name).value == '0'
        assert Race.Races(race.race_name).label == 'Эльф'
        assert Race.Races(race.race_name).name == 'ELF'
        assert Race.objects.filter(race_name=Race.Races.ELF).count() >= 1

        obj2 = Race(race_name=Race.Races.ANGEL)
        assert obj2.get_race_name_display() == obj2.Races(obj2.race_name).label

    # проверяем, что страница по нужному адресу
    def test_get_absolute_url(self):
        race = Race.objects.get(id=self.race.id)
        expected_url = '/races/' + str(self.race.id) + '/'
        # This will also fail if the urlconf is not defined.
        self.assertEquals(race.get_absolute_url(), expected_url)

    def tearDown(self):
        self.race.delete()


# Тесты на модель и views для Owner
class OwnerModelTest(TestCase):
    @classmethod
    # инициализация - создается тестовая БД и в ней объекты User, Owner, Person c тестовыми данными
    def setUp(cls):
        cls.user = get_user_model().objects.create_user(
            username='reviewuser',
            email='reviewuser@email.com',
            password='testpass123'
        )

        cls.special_permission = Permission.objects.get(codename='can_edit_owners')

        cls.owner = Owner.objects.create(
            owner_name='Test',
            owner_description='Test_description',
            link='test_link',
            owner_status='0',
            owner_img='media/euploads/python.png'
        )

    def tearDown(self):
        self.owner.delete()

    # проверяем, что объект с заданным именем был создан и у него параметры как мы передавали
    def test_read_owner(self):
        owner = Owner.objects.get(id=self.owner.id)
        self.assertEqual(owner.owner_name, 'Test')
        self.assertEqual(owner.owner_description, 'Test_description')
        self.assertEqual(owner.link, 'test_link')
        self.assertEqual(owner.owner_status, '0') # Этот тест не нужен, т.к owner_status пересчитывается по существовангию свободных персов
        print('----owners-----------')
        print(dir(self.owner))

    # проверяем, что страница по нужному адресу
    def test_get_absolute_url(self):
        owner = Owner.objects.get(id=self.owner.id)
        expected_url = '/owners/' + str(self.owner.id) + '/'
        # This will also fail if the urlconf is not defined.
        self.assertEquals(owner.get_absolute_url(), expected_url)

    # проверяем, что обновление выполняется
    def test_update_owner(self):
        owner = Owner.objects.get(id=self.owner.id)
        owner.owner_description = 'new description'
        owner.owner_name = 'New name'
        owner.link = 'New link'
        owner.owner_status = '0'
        owner.save()
        updated_owner = Owner.objects.get(id=self.owner.id)
        self.assertEqual(updated_owner.owner_description, 'new description')
        self.assertEqual(updated_owner.owner_name, 'New name')
        self.assertEqual(updated_owner.link, 'New link')
        self.assertEqual(updated_owner.owner_status, '0')


 # Тесты на модель и views для Person
class PersonModelTest(TestCase):
    @classmethod
    # инициализация - создается тестовая БД и в ней объекты User, Owner, Person c тестовыми данными
    def setUp(cls):
        # БД создаем тестовую запись Person
        my_owner = Owner.objects.get(id=cls.owner.id)
        my_race = Race.objects.get(id=cls.race.id)
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

    # проверяем, что объект с заданным именем был создан и у него параметры как мы передавали


def test_read_person(self):
    person = Person.objects.get(id=self.person.id)
    self.assertEqual(person.person_name, 'Test_Person')
    # self.assertEqual(person.owner, self.owner)
    self.assertEqual(person.link, 'Test_person_link')
    self.assertEqual(person.biography, 'test_biography')
    self.assertEqual(person.character, 'test_character')
    self.assertEqual(person.interests, 'test_interests')
    self.assertEqual(person.phobias, 'test_phobias')
    # self.assertEqual(person.race, self.race)
    self.assertEqual(person.location_birth, 1)
    self.assertEqual(person.birth_date, '22.10.2022')
    self.assertEqual(person.location_death, 1)
    self.assertEqual(person.death_date, '22.10.2022')
    self.assertEqual(person.status, 1)
    print('----persons-----------')
    print(dir(self.person))


    # проверяем, что страница по нужному адресу


def test_get_absolute_url(self):
    person = Person.objects.get(id=self.person.id)
    expected_url = '/persons/' + str(self.person.id) + '/'
    # This will also fail if the urlconf is not defined.
    self.assertEquals(person.get_absolute_url(), expected_url)

    # проверяем, что обновление выполняется


def test_update_person(self):
    person = Person.objects.get(id=self.person.id)
    person.person_name = 'Test_Person_new',
    person.person_img = tempfile.NamedTemporaryFile(suffix=".png").name,
   # У персонажа игрока и расу менять нельзя, поэтому в тестирование только проверку на то что не изменилось
    person.link = 'Test_person_link_new',
    person.biography = 'test_biography_new',
    person.character = 'test_character_new',
    person.interests = 'test_interests_new',
    person.phobias = 'test_phobias_new',

    person.location_birth = 2,
    person.birth_date = '22.10.2023',
    person.location_death = 3,
    person.death_date = '22.10.2023',
    person.status = 0
    person.save()
    updated_person = Person.objects.get(id=self.person.id)
    self.assertEqual(updated_person.person_name, 'Test_Person_new')
    self.assertEqual(updated_person.owner.owner_name, self.owner_name)
    self.assertEqual(updated_person.link, 'Test_person_link_new')
    self.assertEqual(updated_person.biography, 'test_biography_new')
    self.assertEqual(updated_person.character, 'test_character_new')
    self.assertEqual(updated_person.interests, 'test_interests_new')
    self.assertEqual(updated_person.phobias, 'test_phobias_new')
    self.assertEqual(updated_person.race.race_name, self.race_name)

def tearDown(self):
        self.person.delete()