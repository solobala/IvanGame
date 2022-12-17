from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import SimpleTestCase
from mysite.poll.models import Owner, Person
from mysite.poll.forms import NewUserForm
from django.urls import reverse, resolve
from mysite.poll.views import index


# Create your tests here.

# Тест на добавление новых пользователей игры
# class CustomUserTests(TestCase):
#
#     def test_create_user(self):
#         User = get_user_model()
#         user = User.objects.create_user(
#             username='will',
#             email='will@email.com',
#             password='testpass123'
#         )
#         self.assertEqual(user.username, 'will')
#         self.assertEqual(user.email, 'will@email.com')
#         self.assertTrue(user.is_active)
#         self.assertFalse(user.is_staff)
#         self.assertFalse(user.is_superuser)
#
#     def test_create_superuser(self):
#         User = get_user_model()
#         admin_user = User.objects.create_superuser(
#             username='gameadmin',
#             email='superadmin@email.com',
#             password='testpass123'
#         )
#         self.assertEqual(admin_user.username, 'superadmin')
#         self.assertEqual(admin_user.email, 'superadmin@email.com')
#         self.assertTrue(admin_user.is_active)
#         self.assertTrue(admin_user.is_staff)
#         self.assertTrue(admin_user.is_superuser)
# #
#
# # Тест на страницы, не использующие модели данных (пример)
# class IndexTests(SimpleTestCase):
#
#     def setUp(self):
#         url = reverse('home')
#         self.response = self.client.get(url)
#
#     # тест на наличие такой страницы по указанному адресу
#     def test_index_status_code(self):
#         self.assertEqual(self.response.status_code, 200)
#
#     # тест на использование правильного шаблона
#     def test_index_template(self):
#         self.assertTemplateUsed(self.response, 'home.html')
#
#     def test_index_contains_correct_html(self):
#         self.assertContains(self.response, 'Homepage')
#
#     def test_index_does_not_contain_incorrect_html(self):
#         self.assertNotContains(
#             self.response, 'Hi there! I should not be on the page.')
#
#     def test_index_url_resolves_indexview(self):  # new
#         view = resolve('/')
#         self.assertEqual(
#             view.func.__name__,
#             index().as_view().__name__
#         )
#
#
# # Тест на странице регистрации
# class RegisterPageTests(TestCase):
#     def setUp(self):
#         url = reverse('register')
#         self.response = self.client.get(url)
#
#     def test_register_template(self):
#         self.assertEqual(self.response.status_code, 200)
#         self.assertTemplateUsed(self.response, 'poll/register.html')
#         self.assertContains(self.response, 'Sign Up')
#         self.assertNotContains(
#             self.response, 'Hi there! I should not be on the page.')
#
#     def test_register_form(self):  # new
#         form = self.response.context.get('form')
#         self.assertIsInstance(form, NewUserForm)
#         self.assertContains(self.response, 'csrfmiddlewaretoken')
#
#     def test_register_request_view(self):  # new
#         view = resolve('/accounts/register/')
#         self.assertEqual(
#             view.func.__name__,
#             register_request().__name__
#         )
#
#
# # Тесты на модель и views для Owner
# class OwnerTests(TestCase):
#
#     # инициализация - создается тестовая БД и в ней объекты User, Owner, Person c тестовыми данными
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             username='reviewuser',
#             email='reviewuser@email.com',
#             password='testpass123'
#         )
#
#         self.special_permission = Permission.objects.get(codename='special_status')
#
#         self.owner = Owner.objects.create(
#             owner_name='Test',
#             owner_description='Test_description',
#             link='test_link',
#             owner_status='1',
#             owner_img='media/euploads/python.png'
#         )
#
#         self.person = Person.objects.create(
#             person_name='Test_Person',
#             person_img='media/euploads/python.png',
#             owner=self.owner,
#             link='Test_person_link',
#             biography='test_biography',
#             character='test_character',
#             interests='test_interests',
#             phobias='test_phobias',
#             race=1,
#             location_birth=1,
#             birth_date='22.10.2022',
#             location_death=1,
#             death_date='22.10.2022',
#             status=1
#         )
#
#     # проверяем, что объект с заданным именем был создан
#     def test_create_owner(self):
#         owner = Owner.objects.get(id=1)
#         expected_object_name = f'{owner.text}'
#         self.assertEqual(expected_object_name, 'just a test')
#
#     #  проверяем, что значения полей этого объекта соответствуют тестовым
#     def test_owner_listing(self):
#         self.assertEqual(f'{self.owner.owner_name}', 'Test')
#         self.assertEqual(f'{self.owner.owner_description}', 'Test_description')
#         self.assertEqual(f'{self.owner.link}', 'test_link')
#         self.assertEqual(f'{self.owner.owner_status}', '1')
#         self.assertEqual(f'{self.owner.owner_img}', 'media/euploads/python.png')
#
#     # Проверяем, что при просмотре списка owners_list в тестовой базе
#     # зарегистрированному пользователю с правом доступа выведется тестовый owner
#     def test_book_list_view_for_logged_in_user(self):
#         self.client.login(email='reviewuser@email.com', password='testpass123')
#         response = self.client.get(reverse('owners-list'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Test')
#         self.assertTemplateUsed(response, 'poll/owner/owners_list.html')
#
#     # Проверяем, что при просмотре списка owners_list в тестовой базе
#     # незарегистрированному пользователю ничего не выведется, и он будет отправлен на страницу входа
#     def test_owner_list_view_for_logged_out_user(self):  # new
#         self.client.logout()
#         response = self.client.get(reverse('owners-list'))
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(
#             response, '%s?next=/owner/' % (reverse('login')))
#         response = self.client.get(
#             '%s?next=/owner/' % (reverse('login')))
#         self.assertContains(response, 'Log In')
#
#     # Проверяем, что при просмотре owner в тестовой базе
#     # зарегистрированному пользователю с правом доступа выведется тестовый owner
#     def test_owner_detail_view_with_permissions(self):
#         self.client.login(email='reviewuser@email.com', password='testpass123')
#         self.user.user_permissions.add(self.special_permission)
#         response = self.client.get(self.owner.get_absolute_url())
#         no_response = self.client.get('/owner/12345/')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(no_response.status_code, 404)
#         self.assertContains(response, 'Test')
#         self.assertContains(response, 'An excellent review')
#         self.assertTemplateUsed(response, 'poll/owner/owner_detail.html')
#
#     # проверяем, что при просмотре owner в тестовой базе
#     #  выведется тестовый owner
#     def test_owner_detail_view(self):
#         response = self.client.get(self.owner.get_absolute_url())
#         no_response = self.client.get('/owner/12345/')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(no_response.status_code, 404)
#         self.assertContains(response, 'Test')
#         self.assertTemplateUsed(response, 'poll/owner/owner_detail.html')
#
#     def test_owner_update_view(self):  # new
#         response = self.client.post(reverse('owner-update', args='0'), {
#             'owner_name':'Test',
#             'owner_description': 'Test_description',
#             'link': 'test_link',
#             'owner_status': '1',
#             'owner_img': 'media/euploads/python.png'
#         })
#         self.assertEqual(response.status_code, 000)
#
#     def test_owner_delete_view(self):  # new
#         response = self.client.get(
#             reverse('owner-delete', args='0'))
#
#         self.assertEqual(response.status_code, 000)
