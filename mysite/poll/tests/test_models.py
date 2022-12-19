from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import SimpleTestCase

from ..models import Owner, Person, Race
from ..forms import NewUserForm
from django.urls import reverse, resolve
from ..views import index
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.mysite.settings")

# Create your tests here.

# Тест на добавление новых пользователей игры
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
#


# Тесты на модель и views для Owner
class OwnerModelTest(TestCase):

    @classmethod
    # инициализация - создается тестовая БД и в ней объекты User, Owner, Person c тестовыми данными
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='reviewuser',
            email='reviewuser@email.com',
            password='testpass123'
        )

        self.special_permission = Permission.objects.get(codename='can_edit_owners')

        self.owner = Owner.objects.create(
            owner_name='Test',
            owner_description='Test_description',
            link='test_link',
            owner_status='1',
            owner_img='media/euploads/python.png'
        )

        # self.person = Person.objects.create(
        #     person_name='Test_Person',
        #     person_img='media/euploads/python.png',
        #     owner=self.owner,
        #     link='Test_person_link',
        #     biography='test_biography',
        #     character='test_character',
        #     interests='test_interests',
        #     phobias='test_phobias',
        #     race=Race.objects.get(race_name='Человек').id,
        #     location_birth=1,
        #     birth_date='22.10.2022',
        #     location_death=1,
        #     death_date='22.10.2022',
        #     status=1
        # )

    # проверяем, что объект с заданным именем был создан
    def test_create_owner(self):
        owner = Owner.objects.get(id=self.owner.id)
        expected_object_name = f'{owner.owner_name}'
        self.assertEqual(expected_object_name, 'Test')

    # проверяем, что страница по нужному адресу
    def test_get_absolute_url(self):
        owner = Owner.objects.get(id=self.owner.id)
        expected_url = '/owner/' + str(self.owner.id)+'/'
        # This will also fail if the urlconf is not defined.
        self.assertEquals(owner.get_absolute_url(), expected_url)