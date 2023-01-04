from django.template.defaulttags import url
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views
from .views import OwnerCreateView, OwnerDeleteView, OwnersListView, \
    OwnersFreeListView, PersonBarDetailView, ActionDetailView, \
    ActionsListView, ActionUpdateView, ActionDeleteView, ActionCreateView, FeatureCreateView, FeatureUpdateView, \
    FeatureDeleteView, FractionDetailView, FractionUpdateView, FractionDeleteView, FractionsListView,  \
    FractionCreateView, ZonesListView, ZoneDetailView, ZoneCreateView, ZoneDeleteView, ZoneUpdateView

from .views import PersonDetailView, PersonCreateView, PersonUpdateView, PersonDeleteView
from .views import PersonsListView,  StatusPersonsListView, FeaturesListView, FeatureDetailView
from .views import MembershipListView, MembershipDeleteView, MembershipUpdateView
from .views import GroupsListView, GroupCreateView, GroupUpdateView, GroupDeleteView, GroupDetailView
from .views import RaceCreateView, RaceUpdateView, RaceDeleteView, RaceDetailView, RacesListView
from .views import LocationsListView, LocationCreateView, LocationUpdateView, LocationDeleteView, LocationDetailView
from .views import RegionsListView, RegionCreateView, RegionUpdateView, RegionDeleteView, RegionDetailView
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
router.register(r'history', views.HistoryViewSet)
router.register(r'personbar', views.PersonBarViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    # path('poll/', views.index, name='index'),

    # path('poll/groups/', views.group, name='group'),



    path('owners/', OwnersListView.as_view(), name='owners-list'),  # список игроков

    path('free_owners/', OwnersFreeListView.as_view(), name='free-owners-list'),
    path('owners/add/', OwnerCreateView.as_view(), name='owner-add'),  # new - не работает

    path("owners/<int:pk>/", views.OwnerDetailView.as_view(), name="owner-detail", ),
    path("owners/<int:pk>/update/", views.OwnerUpdateView.as_view(), name="owner-update", ),
    path('owners/<int:pk>/delete/', OwnerDeleteView.as_view(), name='owner-delete'),  # удаление


    path('register/', views.register_request, name='register'),
    path('login/', views.login_request, name="login"),
    path('logout/', views.logout_request, name="logout"),
    # path("password_reset", views.password_reset_request, name="password_reset"),
    path("password/", views.password_reset_request, name="password_reset"),
    # path('accounts/password_reset/', views.password_reset_request, name='password_reset'),

    path('persons/', PersonsListView.as_view(), name='persons-list'),
    path('<status>/persons/', StatusPersonsListView.as_view(), name='status_persons_list_<status>'),


    path('persons/add/', PersonCreateView.as_view(), name='person-add'),  # new
    path('persons/<int:pk>/', PersonDetailView.as_view(), name='person-detail'),  # просмотр карточки персонажа
    path('personsother/<int:pk>/', PersonDetailView.as_view(), name='other-person-detail'),  # чужого персонажа
    path('persons/<int:pk>/personbar/', PersonBarDetailView.as_view(), name='person-bar-detail'),    # персонажа
    path('persons/<int:pk>/update/', PersonUpdateView.as_view(), name='person-update'),  # обновление
    path('persons/<int:pk>/delete/', PersonDeleteView.as_view(), name='person-delete'),  # удаление

    path('groups/add/', GroupCreateView.as_view(), name='group-add'),  # создание группы
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),  # просмотр карточки группы
    path('groups/<int:pk>/update/', GroupUpdateView.as_view(), name='group-update'),  # редактирование имени группы
    path('groups/<int:pk>/delete/', GroupDeleteView.as_view(), name='group-delete'),
    path('groups/', GroupsListView.as_view(), name='groups-list'),

    path('persons/<int:pk>/membership-delete/', MembershipDeleteView.as_view(), name='membership-delete'),

    path('persons/<int:pk>/membership-update/', MembershipUpdateView.as_view(), name='membership-update'),
    path('persons/<int:pk>/membership/', MembershipListView.as_view(), name='membership-list'),

    path('actions/<int:pk>/', ActionDetailView.as_view(), name='action-detail'),  # просмотр карточки действия
    path('actions/<int:pk>/update', ActionUpdateView.as_view(), name='action-update'),  # обновление действия
    path('actions/<int:pk>/delete', ActionDeleteView.as_view(), name='action-delete'),  # удаление действия
    path('actions/add/', ActionCreateView.as_view(), name='action-add'),  # new action
    path('actions/', ActionsListView.as_view(), name='actions-list'),  # просмотр списка действий

    path('fractions/<int:pk>/', FractionDetailView.as_view(), name='fraction-detail'),  # просмотр карточки свойства
    path('fractions/<int:pk>/update', FractionUpdateView.as_view(), name='fraction-update'),  # обновление свойства
    path('fractions/<int:pk>/delete', FractionDeleteView.as_view(), name='fraction-delete'),  # удаление свойства
    path('fractions/add/', FractionCreateView.as_view(), name='fraction-add'),  # new свойства
    path('fractions/', FractionsListView.as_view(), name='fractions-list'),  # просмотр списка действий

    path('features/<int:pk>/', FeatureDetailView.as_view(), name='feature-detail'),  # просмотр карточки свойства
    path('features/<int:pk>/update', FeatureUpdateView.as_view(), name='feature-update'),  # обновление свойства
    path('features/<int:pk>/delete', FeatureDeleteView.as_view(), name='feature-delete'),  # удаление свойства
    path('features/add/', FeatureCreateView.as_view(), name='feature-add'),  # new свойства
    path('features/', FeaturesListView.as_view(), name='features-list'),  # просмотр списка свойства

    path('locations/<int:pk>/', LocationDetailView.as_view(), name='location-detail'),  # просмотр карточки location
    path('locations/<int:pk>/update', LocationUpdateView.as_view(), name='location-update'),  # обновление location
    path('locations/<int:pk>/delete', LocationDeleteView.as_view(), name='location-delete'),  # удаление location
    path('locations/add/', LocationCreateView.as_view(), name='location-add'),  # new location
    path('locations/', LocationsListView.as_view(), name='locations-list'),  # просмотр списка location

    path('races/', RacesListView.as_view(), name='races-list'),  # список Рас
    path('races/<int:pk>/', RaceDetailView.as_view(), name='race-detail'),  # просмотр карточки расы
    path('races/<int:pk>/update/', RaceUpdateView.as_view(), name='race-update'),  # обновление карточки расы
    path('races/<int:pk>/delete/', RaceDeleteView.as_view(), name='race-delete'),  # удаление
    path('races/add/', RaceCreateView.as_view(), name='race-add'),  # добавить расу

    path('zones/', ZonesListView.as_view(), name='zones-list'),  # список зон
    path('zones/<int:pk>/', ZoneDetailView.as_view(), name='zone-detail'),  # просмотр карточки зоны
    path('zones/<int:pk>/update/', ZoneUpdateView.as_view(), name='zone-update'),  # обновление карточки зоны
    path('zones/<int:pk>/delete/', ZoneDeleteView.as_view(), name='zone-delete'),  # удаление
    path('zones/add/', ZoneCreateView.as_view(), name='zone-add'),  # добавить зону

    path('regions/', RegionsListView.as_view(), name='regions-list'),  # список регионов
    path('regions/<int:pk>/', RegionDetailView.as_view(), name='region-detail'),  # просмотр карточки региона
    path('regions/<int:pk>/update/', RegionUpdateView.as_view(), name='region-update'),  # обновление карточки региона
    path('regions/<int:pk>/delete/', RegionDeleteView.as_view(), name='region-delete'),  # удаление
    path('regions/add/', RegionCreateView.as_view(), name='region-add'),  # добавить региона

    path('owners/', views.OwnerList.as_view()),
    path('owners/<int:pk>/', views.OwnerDetail.as_view()),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
urlpatterns += router.urls
