import json

from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout  # add this
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
# from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.exceptions import EmptyResultSet, PermissionDenied, ValidationError
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from rest_framework import viewsets
from .models import *

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import NewUserForm, ActionUpdateForm, FeatureUpdateForm, OwnerForm, ConsumableForm
from django.http import JsonResponse
from django.urls import reverse
from rest_framework import generics
from . import slovar
from .forms import PersonFormSet

# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework import status

# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from collections import namedtuple
# from .serializers import *
from .slovar import dict_points
from .views1 import *


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("poll:index")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="poll/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.info(request, f"Вы вошли в систему как {username}.")
                return redirect("poll:index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="poll/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    # messages.info(request, "До свидания!")
    return redirect("poll:login")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"

                    email_template_name = "poll/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'solobala@yandex.ru', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()

    return render(request=request, template_name="poll/password/password_reset.html",
                  context={"password_reset_form": password_reset_form})


def index(request):
    """
    Функция отображения для страницы игрока, вошедшего в систему.
    Возвращается вся актуальная информация по всем персонажам игрока
    """
    # CONTEXT надо переписывать, а то последний персонаж затирает все предыдущие, а над чтобы все там были
    context = dict()
    participants = []
    person_properties = dict()

    context['owners'] = Owner.objects.all().order_by("owner_name")
    context['persons'] = Person.objects.all().order_by("person_name")
    context['free_owners'] = Owner.objects.filter(person__status=1).distinct('owner_name')
    context['num_owners'] = Owner.objects.all().count()
    context['num_persons'] = Person.objects.all().count()
    context['num_owners_available'] = Owner.objects.filter(person__status=1).distinct('owner_name').count()
    context['num_persons_available'] = Person.objects.filter(status=1).count()
    context['num_persons_buzy'] = Person.objects.filter(status=2).count()
    context['num_persons_freezed'] = Person.objects.filter(status=0).count()
    if request.user.username != "gameadmin":
        try:
            ow = Owner.objects.get(created_by=request.user)
            persons = ow.person_set.all()
            context['owner_detail'] = ow
            context['owner_status_'] = ['Занят' if context['owner_detail'].owner_status == '1' else 'Свободен'][0]
            context['person_detail'] = persons

            person_spells = dict()
            #  -------------------------------------------------------------------------------------------------------------
            # Для каждого из персонажей считаем статистики
            #  -------------------------------------------------------------------------------------------------------------
            for person in persons:

                inventory_things_sum_weight = 0
                inventory_things_sum_value = 0
                inventory_consumables_sum_weight = 0
                inventory_consumables_sum_value = 0
                inventory_money_sum_weight = 0
                inventory_money_sum_value = 0
                inventory_sum_weight = 0
                inventory_sum_value = 0
                safe_things_sum_weight = 0
                safe_things_sum_value = 0
                safe_consumables_sum_weight = 0
                safe_consumables_sum_value = 0
                safe_money_sum_weight = 0
                safe_money_sum_value = 0
                safe_sum_weight = 0
                safe_sum_value = 0
                sum_weight = 0
                sum_value = 0
                properties = dict()
                safe_stat = {}
                inventory_stat = {}
                person_spells = person.spell_set.all()
                properties["spells"] = person_spells
                #  ---------------------------------------------------------------------------------------------------------
                # по сейфу - он у каждого персонажа только один или его нет вообще
                #  ---------------------------------------------------------------------------------------------------------
                try:
                    safe = Safe.objects.get(person=person.id)
                    # арефакты в сейфе
                    safe_things = safe.things.all()
                    # расходники в сейфе
                    safe_consumables = safe.consumables.all()
                    # деньги в сейфe
                    safe_money = safe.money.all()
                    # суммарно вес и стоимость артефактов  в сейфе
                    for element in safe_things:
                        safe_things_sum_weight += element.weight
                        safe_things_sum_value += element.sale_price
                    # суммарно вес и стоимость расходников в сейфе
                    for element in safe_consumables:
                        safe_consumables_sum_weight += element.weight
                        safe_consumables_sum_value += element.sale_price
                    # суммарно вес и стоимость денег в сейфе
                    for element in safe_money:
                        safe_money_sum_weight += element.weight
                        safe_money_sum_value += element.rate
                    # вес сейфа и стоимость сейфа
                    safe_sum_weight = safe_things_sum_weight + safe_consumables_sum_weight + safe_money_sum_weight
                    safe_sum_value = safe_things_sum_value + safe_consumables_sum_value + safe_money_sum_value

                    safe_stat["safe_sum_weight"] = safe_sum_weight
                    safe_stat["safe_sum_value"] = safe_sum_value
                    safe_stat["safe_things_sum_weight"] = safe_things_sum_weight
                    safe_stat["safe_things_sum_value"] = safe_things_sum_value
                    safe_stat["safe_consumables_sum_weight"] = safe_consumables_sum_weight
                    safe_stat["safe_consumables_sum_value"] = safe_consumables_sum_value
                    safe_stat["safe_money_sum_weight"] = safe_money_sum_weight
                    safe_stat["safe_money_sum_value"] = safe_money_sum_value

                    properties["person"] = person
                    properties["safe"] = safe
                    properties["safe_consumables"] = safe_consumables
                    properties["safe_money"] = safe_money
                    properties["safe_things"] = safe_things
                    properties["safe_stat"] = safe_stat

                except ObjectDoesNotExist:
                    pass

                #  ---------------------------------------------------------------------------------------------------------
                # по рюкзаку:
                #  ---------------------------------------------------------------------------------------------------------
                try:
                    inventory = Inventory.objects.get(person=person.id)
                    inventory_things = inventory.things.all()
                    inventory_consumables = inventory.consumables.all()
                    inventory_money = inventory.money.all()
                    for element in inventory_things:
                        inventory_things_sum_weight += element.weight
                        inventory_things_sum_value += element.sale_price
                    for element in inventory_consumables:
                        inventory_consumables_sum_weight += element.weight
                        inventory_consumables_sum_value += element.sale_price
                    for element in inventory_money:
                        inventory_money_sum_weight += element.weight
                        inventory_money_sum_value += element.rate
                    inventory_sum_weight = inventory_things_sum_weight + \
                                           inventory_consumables_sum_weight + \
                                           inventory_money_sum_weight
                    inventory_sum_value = inventory_things_sum_value + \
                                          inventory_consumables_sum_value + \
                                          inventory_money_sum_value
                    inventory_stat["inventory_sum_weight"] = inventory_sum_weight
                    inventory_stat["inventory_sum_value"] = inventory_sum_value
                    inventory_stat["inventory_things_sum_weight"] = inventory_things_sum_weight
                    inventory_stat["inventory_things_sum_value"] = inventory_things_sum_value
                    inventory_stat["inventory_consumables_sum_weight"] = inventory_consumables_sum_weight
                    inventory_stat["inventory_consumables_sum_value"] = inventory_consumables_sum_value
                    inventory_stat["inventory_money_sum_weight"] = inventory_money_sum_weight
                    inventory_stat["inventory_money_sum_value"] = inventory_money_sum_value
                    properties["inventory"] = inventory
                    properties["inventory_things"] = inventory_things
                    properties["inventory_consumables"] = inventory_consumables
                    properties["inventory_money"] = inventory_money
                    properties["inventory_stat"] = inventory_stat

                except ObjectDoesNotExist:
                    pass
                #  -------------------------------------------------------------------------------------------------------------
                # суммарно
                #  -------------------------------------------------------------------------------------------------------------
                properties["sum_weight"] = inventory_sum_weight + safe_sum_weight
                properties["sum_value"] = inventory_sum_value + safe_sum_value

                if person.group_set.all().exists():
                    context['mygroup'] = True
                    try:
                        gr = person.group_set.all()[0].members.through.objects.filter(
                            group__id=person.group_set.all()[0].pk)
                        # context['inviter'] = gr[0].inviter
                        for membership in gr:
                            participants.append(membership.person)
                        # context['participants'] = participants

                    except ObjectDoesNotExist:
                        pass
                else:
                    context['mygroup'] = False

                try:
                    if person.personlocation_set.all().exists():
                        loca = person.personlocation_set.get(person=person.id)
                        properties["location"] = loca
                except ObjectDoesNotExist:
                    properties["location"] = None

                person_properties[person.id] = properties

        except ObjectDoesNotExist:
            pass
    context['person_properties'] = person_properties
    # print(context)
    return render(request=request, template_name='poll/index.html', context=context)


class JsonableResponseMixin:
    """
    Mixin to add JSON support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)


class OwnerCreateView(LoginRequiredMixin, JsonableResponseMixin, PermissionRequiredMixin, CreateView):
    """
    Добавление нового игрока
    Должно зависеть от того, под каким логином зашли
    """
    model = Owner
    fields = ['owner_name', 'owner_description', 'link']
    login_url = 'poll:login'
    permission_required = 'poll.can_edit_owners'  # new

    def get_context_data(self, **kwargs):
        # we need to overwrite get_context_data
        # to make sure that our formset is rendered
        data = super().get_context_data(**kwargs)

        return data

    def form_valid(self, form):

        form.instance.created_by = self.request.user
        # self.object = form.save()
        owner_amount = Owner.objects.filter(created_by=self.request.user).count()
        if (owner_amount == 0) or (self.request.user.username == 'gameadmin'):  # реальный игрок еще не создал Owner
            context = self.get_context_data()

            return super().form_valid(form)
        else:
            raise PermissionDenied

    def get_success_url(self):
        return reverse("poll:owners-list")


class OwnerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, JsonableResponseMixin, UpdateView):
    """
    Редактирование данных игрока
    """
    model = Owner
    # queryset = Owner.objects.all()
    fields = '__all__'
    template_name_suffix = '_update'
    login_url = 'poll:login'
    permission_required = 'poll.can_edit_owners'  # new

    def form_valid(self, form):
        """
        Сведения о том, кем был изменен игрок
        :param form:
        :return:
        """
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class OwnerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Удаление игрока
    """
    #  model = Owner
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll:owners-list')
    context_object_name = 'owner_detail'
    queryset = Owner.objects.all()
    login_url = 'poll:login'
    permission_required = 'poll.can_delete_owners'  # new

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner_name'] = context['owner_detail'].owner_name
        return context


class OwnerDetailView(LoginRequiredMixin, PermissionRequiredMixin, JsonableResponseMixin, DetailView):
    """
    Просмотр детальной информации по игроку
    """
    template_name = 'poll/owner/owner_detail.html'
    context_object_name = 'owner_detail'
    # model = Owner
    queryset = Owner.objects.all()
    login_url = 'poll:login'
    permission_required = 'poll.can_edit_owners'  # new

    # def get_queryset( self):
    #     """
    #     Просмотр детальной информации по владельцу указанного персонажа
    #     """
    #     selected_person = get_object_or_404(Person, person_name=self.kwargs['person_name'])
    #     context = {'owner_detail': selected_person.owner}
    #     return render(request, 'poll/owner/owner_detail.html', context)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Owner.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner_status_'] = ['Занят' if context['owner_detail'].owner_status == '1' else 'Свободен'][0]
        return context

    def get_success_url(self):
        return reverse_lazy(
            "poll:owner-detail",
            kwargs={"pk": self.object.pk}
        )


class OwnersListView(LoginRequiredMixin, ListView):
    """
    Просмотр полного списка игроков
    """
    template_name = 'poll/owner/owners_list.html'
    context_object_name = 'owners_list'
    queryset = Owner.objects.all()
    login_url = 'poll:login'


class OwnerList(generics.ListCreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    login_url = 'poll:login'


class OwnerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    login_url = 'poll:login'


class OwnerInline:
    form_class = OwnerForm
    model = Owner
    template_name = "owner/owner_create_or_update.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))
        self.object = form.save()
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name, None))
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('poll:owners-list')

    def formset_persons_valid(self, formset):
        persons = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for person in persons:
            person.owner = self.object
            person.save()


class OwnerCreate(OwnerInline, CreateView):
    def get_context_data(self, **kwargs):
        ctx = super(OwnerCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {'persons': PersonFormSet(prefix='persons')}

    def delete_person(request, pk):
        try:
            person = Person.objects.get(id=pk)
        except Person.DoesNotExist:
            messages.success(request, 'Object Does not Exist')
            return redirect('owner: update_owner', pk=person.owner.id)  # Уточнить update_owner или owner-update
        person.delete()
        messages.success(request, 'Персонаж успешно удален')
        return redirect('poll: owner-update', pk=person.owner.id)


class OwnersFreeListView(LoginRequiredMixin, ListView):
    """
    Просмотр списка свободных игроков
    """
    template_name = 'poll/free_owner/free_owners_list.html'
    context_object_name = 'free_owners_list'
    queryset = Owner.objects.filter(person__status=1).distinct('owner_name')
    login_url = 'poll:login'


class PersonCreateView(LoginRequiredMixin, JsonableResponseMixin, CreateView):
    """
    Добавление нового персонажа
    """
    model = Person
    fields = ['person_name', 'person_img', 'owner', 'link', 'biography', 'character', 'interests', 'phobias', 'race',
              'features', 'location_birth', 'birth_date', 'location_death', 'death_date', 'status']
    login_url = 'poll:login'

    def form_valid(self, form):
        """
        Сведения о том, кем был создан персонаж
        :param form:
        :return:
                """
        form.instance.created_by = self.request.user
        owner = get_object_or_404(Owner, id=self.kwargs.get('pk'))
        person = form.save(commit=False)
        person.owner = owner
        form.instance.owner = owner
        person.save()
        return super().form_valid(form)


class PersonUpdateView(LoginRequiredMixin, JsonableResponseMixin, UpdateView):
    """
    Редактирование персонажа
    """
    model = Person
    fields = ['person_name', 'person_img', 'owner', 'link', 'biography', 'character', 'interests', 'phobias', 'race',
              'features', 'location_birth', 'birth_date', 'location_death', 'death_date', 'status']
    template_name_suffix = '_update'
    login_url = 'poll:login'

    def form_valid(self, form):
        """
        Сведения о том, кем был изменен персонаж
        :param form:
        :return:
                """
        form.instance.updated_by = self.request.user

        return super().form_valid(form)


class PersonDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление персонажа
    """
    # model = Person
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll:persons-list')
    context_object_name = 'person_detail'
    queryset = Person.objects.all()
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person_name'] = context['person_detail'].person_name
        return context


class StatusPersonsListView(LoginRequiredMixin, ListView):
    """
    Просмотр  списка свободных персонажей
    """
    template_name = 'poll/person/persons_list.html'

    login_url = 'poll:login'

    def get_context_object_name(self, object_list):
        context_object_name = 'status_persons_list_' + str(self.kwargs['status'])
        return context_object_name

    def get_queryset(self):
        return Person.objects.filter(status=self.kwargs['status'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.kwargs['status']

        return context


class PersonsListView(LoginRequiredMixin, ListView):
    """
    Список Персонажей
    """
    template_name = 'poll/person/persons_list.html'
    context_object_name = 'persons_list'
    queryset = Person.objects.all()
    login_url = 'poll:login'


class GroupDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр информации по конкретной группе
    """
    template_name = 'poll/group/group_detail.html'
    context_object_name = 'group_detail'
    model = Group
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        members = kwargs['object'].members.through.objects.filter(group__id=self.object.pk)
        # members = self.members.through.objects.filter(group__id=self.id)
        context['members'] = members
        try:
            context['inviter_person'] = members[0].inviter
        except members.DoesNotExist:
            context['inviter_person'] = "В группу никто не приглашен"
        return context


class GroupsListView(LoginRequiredMixin, ListView):
    """
    Просмотр списка групп Персонажей
    """
    template_name = 'poll/group/groups_list.html'
    context_object_name = 'groups_list'
    model = Group
    login_url = 'poll:login'


class GroupCreateView(LoginRequiredMixin, JsonableResponseMixin, CreateView):
    """
    Создание новой группы
    """
    template_name = 'add/group_form.html'
    model = Group
    context_object_name = 'Group'
    fields = ['group_name', 'members']
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #     members = self.object.members.through.objects.filter(group__id=self.object.pk)
        return context

    def form_valid(self, form):
        """
        Сведения о том, кем была создана группа
        :param form:
        :return:
        """
        form.instance.created_by = self.request.user
        inviter = get_object_or_404(Person, id=self.kwargs.get('pk'))
        group = form.save(commit=False)
        members = group.members.all()
        for member in members:
            member.through.membership.inviter = inviter

        form.instance.group = group
        group.save()
        return super().form_valid(form)


class GroupUpdateView(LoginRequiredMixin, UpdateView):
    """
    Редактирование группы
    """
    model = Group
    fields = ['group_name', 'members']
    template_name_suffix = '_update'
    login_url = 'poll:login'

    def form_valid(self, form):
        """
        Сведения о том, кем была изменена группа
        :param form:
        :return:
        """
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class GroupDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление группы
    """
    model = Group
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll:groups-list')
    context_object_name = 'group_detail'
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group_name'] = context['group_detail'].group_name
        return context


class MembershipListView(LoginRequiredMixin, ListView):
    """
    Просмотр списка связей
    """
    model = Membership
    template_name = 'poll/membership/members_list.html'
    context_object_name = 'members_list'
    login_url = 'poll:login'


class MembershipDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр информации по конкретному виду связи
    """
    template_name = 'poll/membership/membership_detail.html'
    context_object_name = 'membership_detail'
    model = Membership
    login_url = 'poll:login'


class MembershipCreateView(LoginRequiredMixin, JsonableResponseMixin, CreateView):
    """
    Создание новой связи
    """
    model = Membership
    fields = ['group', 'person', 'inviter', 'invite_reason']
    login_url = 'poll:login'

    def form_valid(self, form):
        """
        Сведения о том, кем была создана связь
        :param form:
        :return:
        """
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class MembershipUpdateView(LoginRequiredMixin, UpdateView):
    """
    Редактирование группы
    """
    model = Membership
    fields = ['group', 'person', 'inviter', 'invite_reason']
    template_name_suffix = '_update'
    login_url = 'poll:login'

    def form_valid(self, form):
        """
        Сведения о том, кем была изменена связь
        :param form:
        :return:
        """
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class MembershipDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление связи
    """
    model = Membership
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll:membership-list')
    context_object_name = 'membership_detail'
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group_name'] = context['membership_detail'].group.group_name
        context['person_name'] = context['membership_detail'].person.person_name
        context['inviter'] = context['membership_detail'].person.membership_invites
        return context


class RacesListView(LoginRequiredMixin, ListView):
    """
    Просмотр полного списка Рас
    """
    template_name = 'poll/race/races_list.html'
    context_object_name = 'races_list'
    model = Race
    login_url = 'poll:login'


class RaceCreateView(LoginRequiredMixin, JsonableResponseMixin, CreateView):
    """
    Создание новой Расы
    """
    model = Race
    fields = '__all__'
    login_url = 'poll:login'

    def form_valid(self, form):
        """
        Сведения о том, кем была создана связь
        :param form:
        :return:
        """
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class RaceUpdateView(LoginRequiredMixin, JsonableResponseMixin, UpdateView):
    """
    Редактирование Расы
    """
    model = Race

    fields = '__all__'
    template_name_suffix = '_update'
    login_url = 'poll:login'
    context_object_name = 'race_update'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        """
        Сведения о том, кем была изменена связь
        :param form:
        :return:
        """
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class RaceDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление Расы
    """
    model = Race
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll:races-list')
    context_object_name = 'race_detail'
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['race_name'] = context['race_detail'].race_name
        return context


class RaceDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр детальной информации по расе
    """
    template_name = 'poll/race/race_detail.html'
    context_object_name = 'race_detail'
    model = Race
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_points = dict()
        for key, value in context['race_detail'].start_points.items():
            start_points[slovar.dict_points.get(key)] = value

        finish_points = dict()
        for key, value in context['race_detail'].finish_points.items():
            finish_points[slovar.dict_points.get(key)] = value

        start_permissions = dict()
        for key, value in context['race_detail'].start_permissions.items():
            start_permissions[slovar.dict_permissions.get(key)] = value

        start_resistances = dict()
        for key, value in context['race_detail'].start_resistances.items():
            start_resistances[slovar.dict_resistances.get(key)] = value

        equipment = dict()
        for key, value in context['race_detail'].equipment.items():
            equipment[slovar.dict_equipment.get(key)] = value

        context['start_points'] = start_points
        context['finish_points'] = finish_points
        context['start_permissions'] = start_permissions
        context['start_resistances'] = start_resistances
        context['equipment'] = equipment
        return context


class PersonBarDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр среза информации по персонажу
    """
    template_name = 'poll/person_bar/person_bar_detail.html'
    context_object_name = 'person_bar_detail'
    model = PersonBar
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['race'] = context['person_bar_detail'].race
        context['person'] = context['person_bar_detail'].person
        for item in context['person_bar_detail'].summary_points:
            context[item[0]] = item
        for item in context['person_bar_detail'].summary_permissions:
            context[item[0]] = item
        for item in context['person_bar_detail'].summary_resistances:
            context[item[0]] = item
        for item in context['person_bar_detail'].summary_equipment:
            context[item[0]] = item
        for item in context['person_bar_detail'].conditions:
            context[item[0]] = item

        return context


class ActionDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр детальной информации по команде
    """
    template_name = 'poll/action/action_detail.html'
    context_object_name = 'action_detail'
    model = Action
    # queryset = Action.objects.all()
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class ActionsListView(LoginRequiredMixin, ListView):
    """
    Просмотр полного списка Действий
    """
    template_name = 'poll/action/actions_list.html'
    context_object_name = 'actions_list'
    model = Action
    login_url = 'poll:login'


class ActionDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление Действия
    """
    model = Action
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll:actions-list')
    context_object_name = 'action_update'
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_name'] = context['action_update'].action_name
        return context


class ActionUpdateView(LoginRequiredMixin, JsonableResponseMixin, UpdateView):
    """
    Редактирование Действия
    """
    model = Action
    form_class = ActionUpdateForm
    context_object_name = 'action_update'
    template_name_suffix = '_update'
    login_url = 'poll:login'

    def actionupdate(self, request, pk):
        action = get_object_or_404(Action, pk=pk)
        if request.method == "POST":
            f = ActionUpdateForm(self.request.POST, instance=action)
            if f.is_valid():
                f.save()
                messages.add_message(request, messages.INFO, 'Action updated.')
                return redirect(reverse('action_update', args=[action.id]))

            # if request is GET the show unbound form to the user, along with data
        else:
            f = ActionUpdateForm(instance=action)

        return render(request, 'poll/action_update.html', {'form': f, 'action': action})

    def form_valid(self, form):
        """
        Сведения о том, кем была изменена связь
        :param form:
        :return:
        """

        form.instance.updated_by = self.request.user

        return super().form_valid(form)


class ActionCreateView(LoginRequiredMixin, JsonableResponseMixin, CreateView):
    """
    Создание нового Действия
    """
    context_object_name = 'action_add'
    model = Action
    # queryset = Action.objects.all()
    template_name = 'add/action_form.html'
    login_url = 'poll:login'
    fields = '__all__'

    # fields = ['action_name', 'action_alias', 'action_description', 'points', 'sp', 'mp', 'ip', 'pp', 'ap', 'fp',
    #           'lp', 'cp', 'bp', 'resistances', 'fire_res', 'water_res', 'wind_res', 'dirt_res', 'lightning_res',
    #           'holy_res', 'curse_res', 'crush_res', 'cut_res', 'stab_res', 'permissions', 'fire_access',
    #           'water_access', 'wind_access', 'dirt_access', 'lightning_access', 'holy_access', 'curse_access',
    #           'bleed_access', 'nature_access', 'mental_access', 'twohanded_access', 'polearm_access',
    #           'onehanded_access',
    #           'stabbing_access', 'cutting_access', 'crushing_access', 'small_arms_access', 'shields_access',
    #           'equipment', 'helmet_status', 'chest_status', 'shoes_status', 'gloves_status', 'item_status']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mydict = dict()
        for key in slovar.dict_points.keys():
            mydict[key] = context['form'].fields.get(key).initial

        if context['form'].fields.get('points').initial is None:
            context['form'].fields['points'].initial = mydict

        mydict = dict()
        for key in slovar.dict_permissions.keys():
            mydict[key] = context['form'].fields.get(key).initial

        if context['form'].fields.get('permissions').initial is None:
            context['form'].fields['permissions'].initial = mydict

        mydict = dict()
        for key in slovar.dict_resistances.keys():
            mydict[key] = context['form'].fields.get(key).initial

        if context['form'].fields.get('resistances').initial is None:
            context['form'].fields['resistances'].initial = mydict

        mydict = dict()
        for key in slovar.dict_equipment.keys():
            mydict[key] = context['form'].fields.get(key).initial

        if context['form'].fields.get('equipment').initial is None:
            context['form'].fields['equipment'].initial = mydict
        return context

    def clean(self):
        cleaned_data = super().clean()
        pk = super().kwargs['pk']
        self.object.update({'action_name': cleaned_data.get('action_name'),
                            'action_alias': cleaned_data.get('action_alias'),
                            'action_description': cleaned_data.get('action_description'),
                            'points': cleaned_data.get('points'),
                            'permissions': cleaned_data.get('permissions'),
                            'resistances': cleaned_data.get('resistances'),
                            'equipment': cleaned_data.get('equipment'),
                            })
        action = Action.objects.get(id=pk)
        action.save()

        if self.request.method == "POST":
            f = ActionCreateView(self.request.POST, instance=action)
            if f.is_valid():
                f.save()
                messages.add_message(self.request, messages.INFO, 'Action updated.')
                return redirect(reverse('action_update', args=[action.id]))

            # if request is GET the show unbound form to the user, along with data
        else:
            f = ActionUpdateForm(instance=action)

        return render(self.request, 'poll/action_update.html', {'form': f, 'action': action})

        # return self.cleaned_data

    def form_valid(self, form):
        """
        Сведения о том, кем была создана связь
        :param form:
        :return:
        """
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class LocationsListView(LoginRequiredMixin, ListView):
    """
    Просмотр полного списка локаций
    """
    template_name = 'poll/location/locations_list.html'
    context_object_name = 'locations_list'
    model = Location
    login_url = 'poll:login'


class LocationCreateView(LoginRequiredMixin, JsonableResponseMixin, CreateView):
    """
    Создание новой Локации
    """
    model = Location
    fields = '__all__'
    login_url = 'poll:login'

    def form_valid(self, form):
        """
        Сведения о том, кем была создана связь
        :param form:
        :return:
        """
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class LocationUpdateView(LoginRequiredMixin, JsonableResponseMixin, UpdateView):
    """
    Редактирование Локации
    """
    model = Location

    fields = '__all__'
    template_name_suffix = '_update'
    login_url = 'poll:login'
    context_object_name = 'location_update'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        """
        Сведения о том, кем была изменена связь
        :param form:
        :return:
        """
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class LocationDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление Локации
    """
    model = Location
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll:locations-list')
    context_object_name = 'location_detail'
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['location_name'] = context['location_detail'].location_name
        return context


class LocationDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр детальной информации по расе
    """
    template_name = 'poll/location/location_detail.html'
    context_object_name = 'location_detail'
    # model = Location
    queryset = Location.objects.all()
    login_url = 'poll:login'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Location.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['location'] = self.object
        return context

    # def get_queryset(self):
    #     return self.object.region_set.all()

    def get_success_url(self):
        return reverse_lazy(
            "/poll/locations/location-detail",
            kwargs={"pk": self.object.pk}
        )


class FeatureDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр детальной информации по Свойству
    """
    template_name = 'poll/feature/feature_detail.html'
    context_object_name = 'feature_detail'
    model = Feature
    # queryset = Feature.objects.all()
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dict_points'] = slovar.dict_points
        context['dict_permissions'] = slovar.dict_permissions
        context['dict_resistances'] = slovar.dict_resistances
        context['dict_equipment'] = slovar.dict_equipment
        return context


class FeaturesListView(LoginRequiredMixin, ListView):
    """
    Просмотр полного списка Свойств
    """
    template_name = 'poll/feature/features_list.html'
    context_object_name = 'features_list'
    queryset = Feature.objects.all()
    login_url = 'poll:login'


class FeatureDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление Свойства
    """
    model = Feature
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll:features-list')
    context_object_name = 'feature_update'
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featuren_name'] = context['feature_update'].feature_name
        return context


class FeatureUpdateView(LoginRequiredMixin, JsonableResponseMixin, UpdateView):
    """
    Редактирование Свойства
    """
    model = Feature
    form_class = FeatureUpdateForm
    context_object_name = 'feature_update'
    template_name_suffix = '_update'
    login_url = 'poll:login'

    def featureupdate(self, request, pk):
        feature = get_object_or_404(Feature, pk=pk)
        if request.method == "POST":
            f = FeatureUpdateForm(self.request.POST, instance=feature)
            if f.is_valid():
                f.save()
                messages.add_message(request, messages.INFO, 'Feature updated.')
                return redirect(reverse('feature_update', args=[feature.id]))
            # if request is GET the show unbound form to the user, along with data
        else:
            f = FeatureUpdateForm(instance=feature)
        return render(request, 'poll/feature_update.html', {'form': f, 'feature': feature})

    def form_valid(self, form):
        """
        Сведения о том, кем была изменена связь
        :param form:
        :return:
        """

        form.instance.updated_by = self.request.user

        return super().form_valid(form)


class FeatureCreateView(LoginRequiredMixin, JsonableResponseMixin, CreateView):
    """
    Создание нового Свойства
    """
    context_object_name = 'feature_add'
    model = Feature
    template_name = 'add/feature_form.html'
    login_url = 'poll:login'
    fields = '__all__'

    def form_valid(self, form):
        """
        Сведения о том, кем была создана связь
        :param form:
        :return:
        """
        return super().form_valid(form)


class FractionsListView(LoginRequiredMixin, ListView):
    """
    Просмотр полного списка Фракций
    """
    template_name = 'poll/fraction/fractions_list.html'
    context_object_name = 'fractions_list'
    model = Fraction
    login_url = 'poll:login'


class FractionCreateView(LoginRequiredMixin, JsonableResponseMixin, CreateView):
    """
    Создание новой Локации
    """
    model = Fraction
    fields = '__all__'
    login_url = 'poll:login'

    def form_valid(self, form):
        """
        Сведения о том, кем была создана Фракции
        :param form:
        :return:
        """
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class FractionUpdateView(LoginRequiredMixin, JsonableResponseMixin, UpdateView):
    """
    Редактирование Фракции
    """
    model = Fraction

    fields = '__all__'
    template_name_suffix = '_update'
    login_url = 'poll:login'
    context_object_name = 'fraction_update'

    def form_valid(self, form):
        """
        Сведения о том, кем была изменена Фракции
        :param form:
        :return:
        """
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class FractionDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление Фракции
    """
    model = Fraction
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll:fractions-list')
    context_object_name = 'fraction_detail'
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fraction_name'] = context['fraction_detail'].fraction_name
        return context


class FractionDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр детальной информации по Фракции
    """
    template_name = 'poll/fraction/fraction_detail.html'
    context_object_name = 'fraction_detail'
    model = Fraction
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class ZonesListView(LoginRequiredMixin, ListView):
    """
    Просмотр полного списка Зон
    """
    template_name = 'poll/zone/zones_list.html'
    context_object_name = 'zones_list'
    model = Zone
    login_url = 'poll:login'


class ZoneCreateView(LoginRequiredMixin, JsonableResponseMixin, CreateView):
    """
    Создание новой Зоны
    """
    model = Zone
    fields = '__all__'
    login_url = 'poll:login'

    def form_valid(self, form):
        """
        Сведения о том, кем была создана Зона
        :param form:
        :return:
        """
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ZoneUpdateView(LoginRequiredMixin, JsonableResponseMixin, UpdateView):
    """
    Редактирование Зоны
    """
    model = Zone

    fields = '__all__'
    template_name_suffix = '_update'
    login_url = 'poll:login'
    context_object_name = 'zone_update'

    def form_valid(self, form):
        """
        Сведения о том, кем была изменена Зона
        :param form:
        :return:
        """
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ZoneDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление Зоны
    """
    model = Zone
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll:zones-list')
    context_object_name = 'zone_detail'
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['zone_name'] = context['zone_detail'].zone_name
        return context


class ZoneDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр детальной информации по Зоне
    """
    template_name = 'poll/zone/zone_detail.html'
    context_object_name = 'zone_detail'
    model = Zone
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class RegionsListView(LoginRequiredMixin, ListView):
    """
    Просмотр полного списка Регионов
    """
    template_name = 'poll/region/regions_list.html'
    context_object_name = 'regions_list'
    model = Region
    login_url = 'poll:login'


class RegionDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр детальной информации по Региону
    """
    template_name = 'poll/region/region_detail.html'
    context_object_name = 'region_detail'
    model = Region
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class RegionUpdateView(LoginRequiredMixin, JsonableResponseMixin, UpdateView):
    """
    Редактирование Региона
    """
    model = Region

    fields = '__all__'
    template_name_suffix = '_update'
    login_url = 'poll:login'

    def form_valid(self, form):
        """
        Сведения о том, кем был изменен Регион
        :param form:
        :return:
        """
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class RegionDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление Региона
    """
    model = Region
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll:regions-list')
    context_object_name = 'region_detail'
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['region_name'] = context['region_detail'].region_name
        return context


class RegionCreateView(LoginRequiredMixin, JsonableResponseMixin, CreateView):
    """
    Создание нового Региона
    """
    model = Region
    fields = '__all__'
    login_url = 'poll:login'

    def form_valid(self, form):
        """
        Сведения о том, кем был создан Регион
        :param form:
        :return:
        """
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class SafesListView(LoginRequiredMixin, ListView):
    """
    Просмотр полного списка Сейфов
    """
    template_name = 'poll/safe/safes_list.html'
    context_object_name = 'safes_list'
    model = Safe
    login_url = 'poll:login'


class SafeDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр детальной информации по Сейфу
    """
    template_name = 'poll/safe/safe_detail.html'
    context_object_name = 'safe_detail'
    model = Safe
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Артефакты в сейфе
        my_things = self.object.things.all()
        # расходники в сейфе
        my_consumables = self.object.consumables.all()
        # ценности в сейфе
        my_money = self.object.money.all()
        consumables_sum_weight = 0
        things_sum_weight = 0
        consumables_sum_value = 0
        things_sum_value = 0
        money_sum_weight = 0
        money_sum_value = 0
        for item in my_things:
            things_sum_weight += item.weight
            things_sum_value += item.sale_price
        for item in my_consumables:
            consumables_sum_weight += item.weight
            consumables_sum_value += item.sale_price
        for item in my_money:
            money_sum_weight += item.weight
            money_sum_value += item.rate
        context['safe_things_sum_weight'] = things_sum_weight
        context['safe_things_sum_value'] = things_sum_value
        context['safe_consumables_sum_weight'] = consumables_sum_weight
        context['safe_consumables_sum_value'] = consumables_sum_value
        context['safe_money_sum_weight'] = money_sum_weight
        context['safe_money_sum_value'] = money_sum_value
        context['safe_sum_weight'] = things_sum_weight + consumables_sum_weight + money_sum_weight
        context['safe_sum_value'] = things_sum_value + consumables_sum_value + money_sum_value
        context['safe_things'] = my_things
        context['safe_consumables'] = my_consumables
        context['safe_money'] = my_money
        return context


class SafeUpdateView(LoginRequiredMixin, JsonableResponseMixin, UpdateView):
    """
    Редактирование Сейфа
    """
    model = Safe

    fields = '__all__'
    template_name_suffix = '_update'
    login_url = 'poll:login'

    def form_valid(self, form):
        """
        Сведения о том, кем был изменен Сейф

        """
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class SafeDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление Сейфа
    """
    model = Safe
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll:safes-list')
    context_object_name = 'safe_detail'
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['safe_name'] = context['safe_detail'].safe_name
        return context


class SafeCreateView(LoginRequiredMixin, JsonableResponseMixin, CreateView):
    """
    Создание нового Сейфа
    """
    template_name = 'add/safe_form.html'
    model = Safe
    fields = '__all__'
    login_url = 'poll:login'

    def form_valid(self, form):
        """
        Сведения о том, кем был создан Сейф
        :param form:
        :return:
        """
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class InventoriesListView(LoginRequiredMixin, ListView):
    """
    Просмотр полного списка Рюкзаков
    """
    template_name = 'poll/inventory/inventories_list.html'
    context_object_name = 'inventories_list'
    model = Inventory
    login_url = 'poll:login'


class InventoryDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр детальной информации по Рюкзаку
    """
    template_name = 'poll/inventory/inventory_detail.html'
    context_object_name = 'inventory_detail'
    model = Inventory
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Артефакты в рюкзаке
        my_things = self.object.things.all()
        # расходники в рюкзаке
        my_consumables = self.object.consumables.all()
        # ценности в рюкзаке
        my_money = self.object.money.all()
        consumables_sum_weight = 0
        things_sum_weight = 0
        consumables_sum_value = 0
        money_sum_weight = 0
        things_sum_value = 0
        money_sum_value = 0
        for item in my_things:
            things_sum_weight += item.weight
            things_sum_value += item.sale_price
        for item in my_consumables:
            consumables_sum_weight += item.weight
            consumables_sum_value += item.sale_price
        for item in my_money:
            money_sum_weight += item.weight
            money_sum_value += item.rate
        amounts = []
        quantities = []
        unique_money = my_money.distinct('money_type', 'rate').values('money_type',
                                                                      'rate')  # уникальные ценности по названию+ номинал
        unique_consumables = my_consumables.distinct('consumable_name',
                                                     'weight')  # уникальные расходники по названию и весу

        for item in unique_money:
            amounts.append(
                my_money.values('money_type', 'rate').annotate(amount=Count('id')))  # количество уникальных ценностей
        for item in unique_consumables:
            quantities.append(my_consumables.values('consumable_name', 'weight').annotate(
                quantity=Count('id')))  # количество уникальных расходников
        print(quantities[0])
        context['quantities'] = quantities[0]
        context['amounts'] = amounts
        context['inventory_things_sum_weight'] = things_sum_weight
        context['inventory_things_sum_value'] = things_sum_value
        context['inventory_consumables_sum_weight'] = consumables_sum_weight
        context['inventory_consumables_sum_value'] = consumables_sum_value
        context['inventory_money_sum_weight'] = money_sum_weight
        context['inventory_money_sum_value'] = money_sum_value
        context['inventory_sum_weight'] = things_sum_weight + consumables_sum_weight + money_sum_weight
        context['inventory_sum_value'] = things_sum_value + consumables_sum_value + money_sum_value
        context['inventory_things'] = my_things
        context['inventory_consumables'] = my_consumables
        context['inventory_money'] = my_money
        print(context['quantities'])
        for pos in context['quantities']:
            for key, value in pos.items():
                print(key, value)
                print
        # print(context['amount'])
        # print(context['quantity'])
        return context


class InventoryUpdateView(LoginRequiredMixin, JsonableResponseMixin, UpdateView):
    """
    Редактирование Рюкзака
    """
    model = Inventory

    fields = '__all__'
    template_name_suffix = '_update'
    login_url = 'poll:login'

    def form_valid(self, form):
        """
        Сведения о том, кем был изменен Сейф

        """
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class InventoryDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление Рюкзака
    """
    model = Inventory
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll:inventories-list')
    context_object_name = 'inventory_detail'
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inventory_name'] = context['inventory_detail'].inventory_name
        return context


class InventoryCreateView(LoginRequiredMixin, JsonableResponseMixin, CreateView):
    """
    Создание нового Сейфа
    """
    template_name = 'add/inventory_form.html'
    model = Inventory
    fields = '__all__'
    login_url = 'poll:login'

    def form_valid(self, form):
        """
        Сведения о том, кем был создан Рюкзак
        :param form:
        :return:
        """
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ThingsListView(LoginRequiredMixin, ListView):
    """
    Просмотр полного списка Артефактов
    """
    template_name = 'poll/thing/things_list.html'
    context_object_name = 'things_list'
    model = Thing
    login_url = 'poll:login'


class ThingDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр детальной информации по Артефакту
    """
    template_name = 'poll/thing/thing_detail.html'
    context_object_name = 'thing_detail'
    model = Thing
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ThingUpdateView(LoginRequiredMixin, JsonableResponseMixin, UpdateView):
    """
    Редактирование Артефакта
    """
    model = Thing

    fields = '__all__'
    template_name_suffix = '_update'
    login_url = 'poll:login'
    context_object_name = 'thing_update'

    def form_valid(self, form):
        """
        Сведения о том, кем был изменен Артефакт

        """
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ThingDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление Артефакта
    """
    model = Thing
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll: things-list')
    context_object_name = 'thing_detail'
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['thing_name'] = context['thing_detail'].thing_name
        return context


class ThingCreateView(LoginRequiredMixin, JsonableResponseMixin, CreateView):
    """
    Создание нового артефакта
    """
    model = Thing
    fields = '__all__'
    login_url = 'poll:login'

    def form_valid(self, form):
        """
        Сведения о том, кем был создан Артефакт
        :param form:
        :return:
        """
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ConsumablesListView(LoginRequiredMixin, ListView):
    """
    Просмотр полного списка Расходников
    """
    template_name = 'poll/consumable/consumables_list.html'
    context_object_name = 'consumables_list'
    model = Consumable
    login_url = 'poll:login'


class ConsumableDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр детальной информации по Расходнику
    """
    template_name = 'poll/consumable/consumable_detail.html'

    context_object_name = 'consumable_detail'
    model = Consumable
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conditions'] = json.loads(context['consumable_detail'].conditions)
        context['points_to_make'] = json.loads(context['consumable_detail'].points_to_make)
        context['points_from_use'] = json.loads(context['consumable_detail'].points_from_use)
        context['resistances_from_use'] = json.loads(context['consumable_detail'].resistances_from_use)
        context['damage_from_use'] = json.loads(context['consumable_detail'].damage_from_use)
        return context


class ConsumableUpdateView(LoginRequiredMixin, JsonableResponseMixin, UpdateView):
    """
    Редактирование Артефакта
    """
    model = Consumable
    context_object_name = 'consumable_update'

    fields = '__all__'
    template_name_suffix = '_update'
    login_url = 'poll:login'

    def form_valid(self, form):
        """
        Сведения о том, кем был изменен расходник

        """
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ConsumableDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление Расходника
    """
    model = Consumable
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll:consumables-list')
    context_object_name = 'consumable_detail'
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['consumable_name'] = context['consumable_detail'].consumable_name

        return context


class ConsumableCreateView(LoginRequiredMixin, JsonableResponseMixin, CreateView):
    model = Consumable
    fields = '__all__'

    login_url = 'poll:login'

    def form_valid(self, form):
        """
        Сведения о том, кем был создан Расходник
        """
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     consumable = Consumable()
    #     consumable.save({'consumable_name': cleaned_data.get('consumable_name'),
    #                     'consumable_description': cleaned_data.get('consumable_description'),
    #                     'points_to_make': cleaned_data.get('points_to_make'),
    #                     'points_from_use': cleaned_data.get('points_from_use'),
    #                     'resistances': cleaned_data.get('resistances'),
    #                     'equipment': cleaned_data.get('equipment'),
    #                         })
    #
    #     if self.request.method == "POST":
    #         f = ConsumableCreateView(self.request.POST, instance=consumable)
    #         if f.is_valid():
    #             f.save()
    #             messages.add_message(self.request, messages.INFO, 'consumable updated.')
    #             return redirect(reverse('consumables-list'))
    #
    #         # if request is GET the show unbound form to the user, along with data
    #     else:
    #         f = ConsumableForm(instance=consumable)
    #
    #     return render(self.request, 'poll/consumable_update.html', {'form': f, 'consumable': consumable})






class MoneyListView(LoginRequiredMixin, ListView):
    """
    Просмотр полного списка Ценностей
    """
    template_name = 'poll/money/money_list.html'
    context_object_name = 'money_list'
    model = Money
    login_url = 'poll:login'


class MoneyCreateView(LoginRequiredMixin, JsonableResponseMixin, CreateView):
    """
    Создание новой Ценности
    """
    model = Money
    fields = '__all__'
    login_url = 'poll:login'

    def form_valid(self, form):
        """
        Сведения о том, кем была создана Ценность
        :param form:
        :return:
        """
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class MoneyUpdateView(LoginRequiredMixin, JsonableResponseMixin, UpdateView):
    """
    Редактирование Ценности
    """
    model = Money

    fields = '__all__'
    template_name_suffix = '_update'
    login_url = 'poll:login'
    context_object_name = 'money_update'

    def form_valid(self, form):
        """
        Сведения о том, кем была изменена Ценность
        :param form:
        :return:
        """
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class MoneyDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление Ценности
    """
    model = Money
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll:money-list')
    context_object_name = 'money_detail'
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['money_type'] = context['money_detail'].money_type
        return context


class MoneyDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр детальной информации по Ценности
    """
    template_name = 'poll/money/money_detail.html'
    context_object_name = 'money_detail'
    model = Money
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class SpellsListView(LoginRequiredMixin, ListView):
    """
    Просмотр полного списка Заклинаний
    """
    template_name = 'poll/spell/spells_list.html'
    context_object_name = 'spells_list'
    model = Spell
    login_url = 'poll:login'


class SpellCreateView(LoginRequiredMixin, JsonableResponseMixin, CreateView):
    """
    Создание нового Заклинания
    """
    model = Spell
    fields = '__all__'
    login_url = 'poll:login'

    def form_valid(self, form):
        """
        Сведения о том, кем было создано Заклинание
        :param form:
        :return:
        """
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class SpellUpdateView(LoginRequiredMixin, JsonableResponseMixin, UpdateView):
    """
    Редактирование Заклинания
    """
    model = Spell

    fields = '__all__'
    template_name_suffix = '_update'
    login_url = 'poll:login'
    context_object_name = 'spell_update'

    def form_valid(self, form):
        """
        Сведения о том, кем была изменено Заклинание
        :param form:
        :return:
        """
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class SpellDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление Фракции
    """
    model = Spell
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll:spells-list')
    context_object_name = 'spell_detail'
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['spell_name'] = context['spell_detail'].spell_name
        return context


class SpellDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр детальной информации по Фракции
    """
    template_name = 'poll/spell/spell_detail.html'
    context_object_name = 'spell_detail'
    model = Spell
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


#  REST API

# nt = namedtuple("object", ["model", "serializers"])
# pattern = {
#     "owner": nt(Owner, OwnerSerializer),
#     "person": nt(Person, PersonSerializer),
#     "race": nt(Race, RaceSerializer),
#     "feature": nt(Feature, FeatureSerializer),
#     "region": nt(Region, RegionSerializer),
#     "zone": nt(Zone, ZoneSerializer),
#     "location": nt(Location, LocationSerializer),
#     "fraction": nt(Fraction, FractionSerializer),
#     "group": nt(Group, GroupSerializer),
#     "personbar": nt(PersonBar, PersonBarSerializer),
#     "action": nt(Action, ActionSerializer),
#     "history": nt(History, HistorySerializer),
# }
#
#
# @api_view(['GET', 'POST'])
# def ListView(request, api_name):
#     object = pattern.get(api_name, None)
#     if object == None:
#         return Response(
#             data="Invalid URL",
#             status=status.HTTP_404_NOT_FOUND,
#         )
#     if request.method == "GET":
#         object_list = object.model.objects.all()
#         serializers = object.serializers(object_list, many=True)
#         return Response(serializers.data)
#
#     if request.method == "POST":
#         data = request.data
#         serializers = object.serializers(data=data)
#
#         if not serializers.is_valid():
#             return Response(
#                 data=serializers.error,
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         serializers.save()
#         return Response(
#             data=serializers.error,
#             status=status.HTTP_201_CREATED
#         )
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def owners_detail(request, pk):
#     """
#  Retrieve, update or delete a customer by id/pk.
#  """
#     try:
#         owner = Owner.objects.get(pk=pk)
#     except Owner.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = OwnerSerializer(owner, context={'request': request})
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = OwnerSerializer(owner, data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         owner.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


class RaceViewSet(viewsets.ModelViewSet):
    queryset = Race.objects.all()
    serializer_class = RaceSerializer


class FractionViewSet(viewsets.ModelViewSet):
    queryset = Fraction.objects.all()
    serializer_class = FractionSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer


class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class PersonBarViewSet(viewsets.ModelViewSet):
    queryset = PersonBar.objects.all()
    serializer_class = PersonBarSerializer


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer


class SafeViewSet(viewsets.ModelViewSet):
    queryset = Safe.objects.all()
    serializer_class = SafeSerializer


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class ThingViewSet(viewsets.ModelViewSet):
    queryset = Thing.objects.all()
    serializer_class = ThingSerializer


class ConsumableViewSet(viewsets.ModelViewSet):
    queryset = Consumable.objects.all()
    serializer_class = ConsumableSerializer


class MoneyViewSet(viewsets.ModelViewSet):
    queryset = Money.objects.all()
    serializer_class = MoneySerializer
