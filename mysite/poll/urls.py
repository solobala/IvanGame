
from django.urls import path, include
from rest_framework.routers import SimpleRouter

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
# router = routers.DefaultRouter() # У меня было так
router = SimpleRouter()  # это пример из youtube


router.register(r'owner', views.OwnerViewSet, basename='owner')
router.register(r'person', views.PersonViewSet, basename='person')
router.register(r'group', views.GroupViewSet)
router.register(r'membership', views.MembershipViewSet)
router.register(r'race', views.RaceViewSet)
router.register(r'region', views.RegionViewSet)
router.register(r'location', views.LocationViewSet)
router.register(r'zone', views.ZoneViewSet)
router.register(r'action', views.ActionViewSet)
router.register(r'fraction', views.FractionViewSet)
router.register(r'feature', views.FeatureViewSet)

urlpatterns = [

    path('poll/', views.index, name='index'),

    # path('poll/group/', views.group, name='group'),

    path('poll/owners/', OwnersListView.as_view(), name='owners-list'),  # список игроков

    path('poll/free_owners/', OwnersFreeListView.as_view(), name='free-owners-list'),
    path('poll/owners/add/', OwnerCreateView.as_view(), name='owner-add'),  # new - не работает
    # path('poll/owner/', OwnerCreate.as_view(), name='create_owner'),  # new - не работает
    path("poll/owners/<int:pk>/", views.OwnerDetailView.as_view(), name="owner-detail", ),
    path("poll/owners/<int:pk>/update/", views.OwnerUpdateView.as_view(), name="owner-update", ),
    path('poll/owners/<int:pk>/delete/', OwnerDeleteView.as_view(), name='owner-delete'),  # удаление

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

    path('poll/persons/', PersonsListView.as_view(), name='persons-list'),
    path('poll/<status>/persons/', StatusPersonsListView.as_view(), name='status_persons_list_<status>'),

       #path('poll/owner/<int:pk>/person/add/', PersonCreateView.as_view(), name='person-add'),  # new
    path('poll/persons/add', PersonCreateView.as_view(), name='person-add'),  # new
    path('poll/persons/<int:pk>/', PersonDetailView.as_view(), name='person-detail'),  # просмотр карточки персонажа
    path('poll/personsother/<int:pk>/', PersonDetailView.as_view(), name='other-person-detail'),  # чужого персонажа
    path('poll/persons/<int:pk>/personbar/', PersonBarDetailView.as_view(), name='person-bar-detail'),    # персонажа
    path('poll/persons/<int:pk>/update/', PersonUpdateView.as_view(), name='person-update'),  # обновление
    path('poll/persons/<int:pk>/delete/', PersonDeleteView.as_view(), name='person-delete'),  # удаление

    path('poll/persons/<int:pk>/group/add/', GroupCreateView.as_view(), name='new_group'),  # new group
    path('poll/groups/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),  # просмотр карточки группы
    path('poll/groups/<int:pk>/update/', GroupUpdateView.as_view(), name='group-update'),  # редактирование имени группы
    path('poll/groups/<int:pk>/delete/', GroupDeleteView.as_view(), name='group-delete'),
    path('poll/groups/', GroupsListView.as_view(), name='groups-list'),

    path('poll/persons/<int:pk>/membership-delete/', MembershipDeleteView.as_view(), name='membership-delete'),
    path('poll/persons/<int:pk>/group-add/', GroupCreateView.as_view(), name='group-add'),  # создание группы
    path('poll/persons/<int:pk>/membership-update/', MembershipUpdateView.as_view(), name='membership-update'),
    path('poll/persons/<int:pk>/membership/', MembershipListView.as_view(), name='membership-list'),

    path('poll/actions/<int:pk>/', ActionDetailView.as_view(), name='action-detail'),  # просмотр карточки действия
    path('poll/actions/<int:pk>/update', ActionUpdateView.as_view(), name='action-update'),  # обновление действия
    path('poll/actions/<int:pk>/delete', ActionDeleteView.as_view(), name='action-delete'),  # удаление действия
    path('poll/actions/add/', ActionCreateView.as_view(), name='action-add'),  # new action
    path('poll/actions/', ActionsListView.as_view(), name='actions-list'),  # просмотр списка действий

    #  path('poll/fraction/', FractionsListView.as_view(), name='fractions-list'),  # просмотр списка действий

    path('poll/features/<int:pk>/', FeatureDetailView.as_view(), name='feature-detail'),  # просмотр карточки свойства
    path('poll/features/<int:pk>/update', FeatureUpdateView.as_view(), name='feature-update'),  # обновление свойства
    path('poll/features/<int:pk>/delete', FeatureDeleteView.as_view(), name='feature-delete'),  # удаление свойства
    path('poll/features/add/', FeatureCreateView.as_view(), name='feature-add'),  # new свойства
    path('poll/features/', FeaturesListView.as_view(), name='features-list'),  # просмотр списка свойства

    path('poll/locations/<int:pk>/', LocationDetailView.as_view(), name='location-detail'),  # просмотр карточки location
    path('poll/locations/<int:pk>/update', LocationUpdateView.as_view(), name='location-update'),  # обновление location
    path('poll/locations/<int:pk>/delete', LocationDeleteView.as_view(), name='location-delete'),  # удаление location
    path('poll/locations/add/', LocationCreateView.as_view(), name='location-add'),  # new location
    path('poll/locations/', LocationsListView.as_view(), name='locations-list'),  # просмотр списка location

    path('poll/races/', RacesListView.as_view(), name='races-list'),  # список Рас
    path('poll/races/<int:pk>/', RaceDetailView.as_view(), name='race-detail'),  # просмотр карточки расы
    path('poll/races/<int:pk>/update/', RaceUpdateView.as_view(), name='race-update'),  # обновление карточки расы
    path('poll/races/<int:pk>/delete/', RaceDeleteView.as_view(), name='race-delete'),  # удаление
    path('poll/races/add/', RaceCreateView.as_view(), name='race-add'),  # добавить расу
    path('owners/', views.OwnerList.as_view()),
    path('owners/<int:pk>/', views.OwnerDetail.as_view()),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
# urlpatterns += router.urls
