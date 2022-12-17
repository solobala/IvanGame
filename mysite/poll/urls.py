
from django.urls import path, include
from . import views
from .views import OwnerCreateView, OwnerDeleteView, OwnersListView, \
    OwnersFreeListView, RaceDetailView, RacesListView, PersonBarDetailView, ActionDetailView, \
    ActionsListView, ActionUpdateView, ActionDeleteView, ActionCreateView, FeatureCreateView, FeatureUpdateView, \
    FeatureDeleteView, OwnerCreate
from .views import PersonDetailView, PersonCreateView, PersonUpdateView, PersonDeleteView
from .views import PersonsListView,  StatusPersonsListView, FeaturesListView, FeatureDetailView
from .views import MembershipListView, MembershipDeleteView, MembershipUpdateView
from .views import GroupsListView, GroupCreateView, GroupUpdateView, GroupDeleteView, GroupDetailView
from .views import RaceCreateView, RaceUpdateView, RaceDeleteView
from .views import LocationsListView, LocationCreateView, LocationUpdateView, LocationDeleteView, LocationDetailView

from rest_framework import routers
app_name = 'poll'

# REST API
router = routers.DefaultRouter()


# router.register(r'owners', views.OwnerViewSet)
# router.register(r'persons', views.PersonViewSet)
# router.register(r'groups', views.GroupViewSet)
# router.register(r'memberships', views.MembershipViewSet)
# router.register(r'races', views.RaceViewSet)

urlpatterns = [

    path('poll/', views.index, name='index'),

    # path('poll/group/', views.group, name='group'),

    path('poll/owner/', OwnersListView.as_view(), name='owners-list'),  # список игроков

    path('poll/free_owner/', OwnersFreeListView.as_view(), name='free-owners-list'),
    path('poll/owner/add/', OwnerCreateView.as_view(), name='owner-add'),  # new - не работает
    path('poll/owner/', OwnerCreate.as_view(), name='create_owner'),  # new - не работает
    path("poll/owner/<int:pk>/", views.OwnerDetailView.as_view(), name="owner-detail", ),
    path("poll/owner/<int:pk>/update/", views.OwnerUpdateView.as_view(), name="owner-update", ),
    path('poll/owner/<int:pk>/delete/', OwnerDeleteView.as_view(), name='owner-delete'),  # удаление

    # path("password_reset", views.password_reset_request, name="password_reset"),
    # path('poll/register/', views.register_request, name='register'),
    # path('poll/login/', views.login_request, name="login"),
    # path('poll/logout/', views.logout_request, name="logout"),
    # path('poll/password_reset', views.password_reset_request, name="password_reset"),

    path("password_reset", views.password_reset_request, name="password_reset"),
    path('accounts/register/', views.register_request, name='register'),
    path('accounts/login/', views.login_request, name="login"),
    path('accounts/logout/', views.logout_request, name="logout"),
    path('accounts/password_reset', views.password_reset_request, name="password_reset"),

    path('poll/person/', PersonsListView.as_view(), name='persons-list'),
    path('poll/<status>/person/', StatusPersonsListView.as_view(), name='status_persons_list_<status>'),

    # path('poll/busy_person/', PersonsBusyListView.as_view(), name='busy-persons-list'),
    # path('poll/free_person/', PersonsFreeListView.as_view(), name='free-persons-list'),
    # path('poll/freez_person/', PersonsFreezListView.as_view(), name='freez-persons-list'),

    #path('poll/owner/<int:pk>/person/add/', PersonCreateView.as_view(), name='person-add'),  # new
    path('poll/person/add', PersonCreateView.as_view(), name='person-add'),  # new
    path('poll/person/<int:pk>/', PersonDetailView.as_view(), name='person-detail'),  # просмотр карточки персонажа
    path('poll/person/other/<int:pk>/', PersonDetailView.as_view(), name='other-person-detail'),  # чужого персонажа
    path('poll/person/<int:pk>/personbar/', PersonBarDetailView.as_view(), name='person-bar-detail'),    # персонажа
    path('poll/person/<int:pk>/update/', PersonUpdateView.as_view(), name='person-update'),  # обновление
    path('poll/person/<int:pk>/delete/', PersonDeleteView.as_view(), name='person-delete'),  # удаление

    path('poll/person/<int:pk>/group/add/', GroupCreateView.as_view(), name='new_group'),  # new group
    path('poll/group/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),  # просмотр карточки группы
    path('poll/group/<int:pk>/update/', GroupUpdateView.as_view(), name='group-update'),  # редактирование имени группы
    path('poll/group/<int:pk>/delete/', GroupDeleteView.as_view(), name='group-delete'),
    path('poll/group/', GroupsListView.as_view(), name='groups-list'),

    path('poll/person/<int:pk>/membership-delete/', MembershipDeleteView.as_view(), name='membership-delete'),
    path('poll/person/<int:pk>/group-add/', GroupCreateView.as_view(), name='group-add'),  # создание группы
    path('poll/person/<int:pk>/membership-update/', MembershipUpdateView.as_view(), name='membership-update'),
    path('poll/person/<int:pk>/membership/', MembershipListView.as_view(), name='membership-list'),

    path('poll/action/<int:pk>/', ActionDetailView.as_view(), name='action-detail'),  # просмотр карточки действия
    path('poll/action/<int:pk>/update', ActionUpdateView.as_view(), name='action-update'),  # обновление действия
    path('poll/action/<int:pk>/delete', ActionDeleteView.as_view(), name='action-delete'),  # удаление действия
    path('poll/action/add/', ActionCreateView.as_view(), name='action-add'),  # new action
    path('poll/action/', ActionsListView.as_view(), name='actions-list'),  # просмотр списка действий

    #  path('poll/fraction/', FractionsListView.as_view(), name='fractions-list'),  # просмотр списка действий

    path('poll/feature/<int:pk>/', FeatureDetailView.as_view(), name='feature-detail'),  # просмотр карточки свойства
    path('poll/feature/<int:pk>/update', FeatureUpdateView.as_view(), name='feature-update'),  # обновление свойства
    path('poll/feature/<int:pk>/delete', FeatureDeleteView.as_view(), name='feature-delete'),  # удаление свойства
    path('poll/feature/add/', FeatureCreateView.as_view(), name='feature-add'),  # new свойства
    path('poll/feature/', FeaturesListView.as_view(), name='features-list'),  # просмотр списка свойства

    path('poll/location/<int:pk>/', LocationDetailView.as_view(), name='location-detail'),  # просмотр карточки location
    path('poll/location/<int:pk>/update', LocationUpdateView.as_view(), name='location-update'),  # обновление location
    path('poll/location/<int:pk>/delete', LocationDeleteView.as_view(), name='location-delete'),  # удаление location
    path('poll/location/add/', LocationCreateView.as_view(), name='location-add'),  # new location
    path('poll/location/', LocationsListView.as_view(), name='locations-list'),  # просмотр списка location

    path('poll/race/', RacesListView.as_view(), name='races-list'),  # список Рас
    path('poll/race/<int:pk>/', RaceDetailView.as_view(), name='race-detail'),  # просмотр карточки расы
    path('poll/race/<int:pk>/update/', RaceUpdateView.as_view(), name='race-update'),  # обновление карточки расы
    path('poll/race/<int:pk>/delete/', RaceDeleteView.as_view(), name='race-delete'),  # удаление
    path('poll/race/add/', RaceCreateView.as_view(), name='race-add'),  # добавить расу

    path('', include(router.urls)),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('owners/', views.OwnerList.as_view()),
    path('owners/<int:pk>/', views.OwnerDetail.as_view()),
]
