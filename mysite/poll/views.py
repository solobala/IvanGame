
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout  # add this
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
#  from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Owner, Person, Group, Membership, Race, PersonBar, Action, Location, Feature
from .serializers import OwnerSerializer, PersonSerializer, GroupSerializer, MembershipSerializer, RaceSerializer
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import NewUserForm, ActionUpdateForm, FeatureUpdateForm
from django.http import JsonResponse
from django.forms.models import inlineformset_factory
from django.urls import reverse

# from django.forms import ModelForm
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.http import Http404
# from rest_framework import mixins
from rest_framework import generics
from . import slovar

# PersonFormset = inlineformset_factory(
#     Owner, Person, fields=('person_name',)
# )


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
    # return render(request=request, template_name="poll/register.html", context={"register_form": form})
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
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("poll:index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="poll/login.html", context={"login_form": form})
    #  return render(request=request, template_name="poll/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("poll:index")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    # email_template_name = "poll/password/password_reset_email.txt"
                    email_template_name = "accounts/password/password_reset_email.txt"
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
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    # return render(request=request, template_name="poll/password/password_reset.html",
    return render(request=request, template_name="accounts/password/password_reset.html",
                  context={"password_reset_form": password_reset_form})


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_owners = Owner.objects.all().count()
    num_persons = Person.objects.all().count()
    # Доступные игроки и персонажи
    num_owners_available = Owner.objects.filter(person__status=1).distinct('owner_name').count()
    num_persons_available = Person.objects.filter(status=1).count()  # Метод 'all()' применён по умолчанию.
    return render(
        request,
        'poll/index.html',
        context={'num_owners': num_owners, 'num_persons': num_persons,
                 'num_owners_available': num_owners_available, 'num_persons_available': num_persons_available},
    )


class OwnerCreateView(LoginRequiredMixin, JsonableResponseMixin, PermissionRequiredMixin, CreateView):
    """
    Добавление нового игрока
    Должно зависеть от того, под каким логином зашли
    """
    model = Owner
    fields = ['owner_name', 'owner_description', 'link']
    login_url = 'poll:login'
    permission_required = 'poll.special_status'  # new
    def get_context_data(self, **kwargs):
        # we need to overwrite get_context_data
        # to make sure that our formset is rendered
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["persons"] = PersonFormset(self.request.POST)
        else:
            data["persons"] = PersonFormset()
        return data

    def form_valid(self, form):

        form.instance.created_by = self.request.user
        # self.object = form.save()
        owner_amount = Owner.objects.filter(created_by=self.request.user).count()
        if owner_amount == 0:  # реальный игрок еще не создал Owner
            context = self.get_context_data()
            persons = context["persons"]

            if persons.is_valid():
                persons.instance = self.object
                persons.save()
            return super().form_valid(form)
        else:  # У игрока уже есть Owner, нового создавать нельзя
            return reverse("Forbidden")

    def get_success_url(self):
        return reverse("owners-list")
    # def form_valid(self, form):
    #     """
    #     Сведения о том, кем был создан игрок
    #     :param form:
    #     :return:
    #     """
    #     form.instance.created_by = self.request.user
    #     return super().form_valid(form)

    # def add_owner(owner_name, owner_description, link):
    #     """
    #     Добавление нового игрока в список
    #     :param owner_name:
    #     :param owner_description:
    #     :param link:
    #     :return:
    #     """
    #     try:
    #         Owner.objects.get(owner_name=owner_name)
    #         response = 'Игрок %s уже существует'
    #     except ObjectDoesNotExist:
    #         b = Owner(owner_name=owner_name, owner_description=owner_description, link=link)
    #         b.save()
    #         response = 'Игрок %s добавлен'
    #     finally:
    #         return HttpResponse(response)


class OwnerUpdateView(LoginRequiredMixin,
                      PermissionRequiredMixin, JsonableResponseMixin, UpdateView):
    """
    Редактирование данных игрока
    """
    model = Owner
    # queryset = Owner.objects.all()
    fields = ['owner_name', 'owner_description', 'link']
    template_name_suffix = '_update'
    login_url = 'poll:login'
    permission_required = 'poll.special_status'  # new
    # def get_context_data(self, **kwargs):
    #     # we need to overwrite get_context_data
    #     # to make sure that our formset is rendered.
    #     # the difference with CreateView is that
    #     # on this view we pass instance argument
    #     # to the formset because we already have
    #     # the instance created
    #     data = super().get_context_data(**kwargs)
    #     if self.request.POST:
    #         data["persons"] = PersonFormset(self.request.POST, instance=self.object)
    #     else:
    #         data["persons"] = PersonFormset(instance=self.object)
    #     return data

    # def manage_books(request, owner_id):
    #     owner = Owner.objects.get(pk=owner_id)
    #     PersonInlineFormSet = inlineformset_factory(Owner, Person, fields=('person_name',))
    #     if request.method == "POST":
    #         formset = PersonInlineFormSet(request.POST, request.FILES, instance=owner)
    #         if formset.is_valid():
    #             formset.save()
    #             # Do something. Should generally end with a redirect. For example:
    #             return HttpResponseRedirect(owner.get_absolute_url())
    #     else:
    #         formset = PersonInlineFormSet(instance=owner)
    #     return render(request, 'manage_books.html', {'formset': formset})

    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     persons = context["persons"]
    #     self.object = form.save()
    #     if persons.is_valid():
    #         persons.instance = self.object
    #         persons.save()
    #     form.instance.updated_by = self.request.user
    #     return super().form_valid(form)

    # def get_success_url(self):
    #     # return reverse("poll:owners-list")
    #     # return reverse("poll:owner-detail")
    #     return reverse_lazy(
    #         "poll:owner-detail", kwargs={"pk": self.object.pk}
    #      )
    def form_valid(self, form):
        """
        Сведения о том, кем был изменен игрок
        :param form:
        :return:
        """
        # ModelFormMixin.success_url = "127.0.0.1:8000/poll/owner/5/owner-detail.html"

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner_name'] = context['owner_detail'].owner_name
        return context


class OwnerDetailView(LoginRequiredMixin,
                      PermissionRequiredMixin, JsonableResponseMixin, DetailView):
    """
    Просмотр детальной информации по игроку
    """
    template_name = 'poll/owner/owner_detail.html'
    context_object_name = 'owner_detail'
    #model = Owner
    queryset = Owner.objects.all()
    login_url = 'poll:login'
    permission_required = 'poll.special_status'  # new

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
        # return reverse("owners-list")
        return reverse_lazy(
            "/poll/owner/owner-detail",
            kwargs={"pk": self.object.pk}
        )

    # def get_queryset(self):
    #     return self.object.person_set.all()


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


class OwnersFreeListView(LoginRequiredMixin, ListView):
    """
    Просмотр списка свободных игроков
    """
    template_name = 'poll/free_owner/free_owners_list.html'
    context_object_name = 'free_owners_list'
    queryset = Owner.objects.filter(person__status=1).distinct('owner_name')
    login_url = 'poll:login'


# class OwnerByPerson(DetailView):
#     """
#        Просмотр детальной информации по игроку, найденному по персонажу
#        """
#     template_name = 'poll/owner/owner_detail.html'
#     context_object_name = 'owner_detail'
#     queryset = Owner.objects.get()


# class OwnerPersonListView(ListView):
#     """
#     Просмотр  списка персонажей игрока
#     """
#     template_name = 'poll/person/persons_by_owner.html'
#     context_object_name = 'persons_by_owner'
#
#     def get_queryset(self):
#         self.owner = get_object_or_404(Owner, owner_name=self.kwargs['owner'])
#         return Person.objects.filter(owner=self.owner)
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         # Add in the publisher
#         context['owner'] = self.owner
#         return context

class PersonCreateView(LoginRequiredMixin, JsonableResponseMixin, CreateView):
    """
    Добавление нового персонажа
    """
    model = Person
    fields = ['person_name', 'person_img', 'owner', 'link', 'biography', 'character', 'interests', 'phobias', 'race',
              'location_birth', 'birth_date', 'location_death', 'death_date', 'status']
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
              'location_birth', 'birth_date', 'location_death', 'death_date', 'status']
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
        context_object_name = 'persons_list_' + str(self.kwargs['status'])
        return context_object_name

    def get_queryset(self):

        return Person.objects.filter(status=self.kwargs['status'])

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.kwargs['status']

        return context



# class PersonsFreeListView(LoginRequiredMixin, ListView):
#     """
#     Просмотр  списка свободных персонажей
#     """
#     template_name = 'poll/free_person/free_persons_list.html'
#
#     context_object_name = 'free_persons_list'
#     queryset = Person.objects.filter(status=1)
#     login_url = 'poll:login'
#
#
# class PersonsBusyListView(LoginRequiredMixin, ListView):
#     """
#     Просмотр  списка занятых персонажей
#     """
#     template_name = 'poll/busy_person/busy_persons_list.html'
#     context_object_name = 'busy_persons_list'
#     queryset = Person.objects.filter(status=0)
#     login_url = 'poll:login'
#
#
# class PersonsFreezListView(LoginRequiredMixin, ListView):
#     """
#     Просмотр  списка заморозки персонажей
#     """
#     template_name = 'poll/freez_person/freez_persons_list.html'
#     context_object_name = 'freez_persons_list'
#     queryset = Person.objects.filter(status=2)
#     login_url = 'poll:login'


class PersonsListView(LoginRequiredMixin, ListView):
    """
    Список Персонажей
    """
    template_name = 'poll/person/persons_list.html'
    context_object_name = 'persons_list'
    queryset = Person.objects.all()
    login_url = 'poll:login'


class PersonDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр информации по персонажу
    """
    template_name = 'poll/person/person_detail.html'
    context_object_name = 'person_detail'
    # queryset = Person.objects.all()
    model = Person
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_'] = ['Свободен' if context['person_detail'].status == 1
                              else 'Занят' if context['person_detail'].status == 2 else 'Заморозка'][0]
        person_group = Person.objects.get(
            id=context['person_detail'].pk).group_set.all()  # Это Queryset - список групп из 1 группы
        amount = person_group.count()  # это к-во групп с нашим персонажем - или 0, или 1
        members = Membership.objects.filter(
            inviter=Person.objects.get(id=context['person_detail'].pk))  # Membership с участием нашего Person
        amount1 = members.count()

        # Person может быть inviter, участник группы или никто
        # Если amount=0 и amount1>1 - наш person - это inviter
        # Если не inviter, но участник группы - >= 1 (число людей в группе), иначе 0
        if amount >= 1:
            context['group_status'] = 'в группе'
            context['inviter_person'] = Membership.objects.filter(group_id=person_group[0].id)[0].inviter
            context['participants'] = person_group[
                0].members.all()  # Queryset список Person - членов гРуппы, без inviter

            # Если не inviter или не состоит в группе - получится 0
        elif amount == 0 and amount1 == 0:
            context['group_status'] = 'не в группе'
            # это inviter
        else:
            context['group_status'] = 'в группе'
            participants = []
            for member in members:
                participants.append(member.person)
            context['inviter_person'] = members[0].inviter
            context['participants'] = participants

        info = Person.objects.get(id=context['person_detail'].pk).personbar_set.all()[0]

        points = dict()
        for key, value in info.summary_points.items():
            points[slovar.dict_points_start.get(key)] = value

        permissions = dict()
        for key, value in info.summary_permissions.items():
            permissions[slovar.dict_permissions_start.get(key)] = value

        resistances = dict()
        for key, value in info.summary_resistances.items():
            resistances[slovar.dict_resistances_start.get(key)] = value

        equipment = dict()
        for key, value in info.summary_equipment.items():
            equipment[slovar.dict_equipment_start.get(key)] = value

        context['summary_points'] = points
        context['summary_permissions'] = permissions
        context['summary_resistances'] = resistances
        context['summary_equipment'] = equipment
        context['unallocated_points'] = info.unallocated_points
        context['unallocated_permissions'] = info.unallocated_permissions

        health = round(25 * (points['Стамина'] * 0.2
                             + points['Интеллект'] * 0.2
                             + points['Сила'] * 0.5
                             + points['Ловкость'] * 0.4
                             + points['Рассудок'] * 0.4
                             + (permissions['Гематомантия'] * 0.1
                                + permissions['Ботаника'] * 0.1
                                + permissions['Псифистика'] * 0.1)) ** 1.5, 0)
        context['health'] = health

        mental_health = round(10 * (points['Интеллект'] * 0.4
                                    + points['Вера'] * 0.3
                                    + points['Рассудок'] * 0.5
                                    + (permissions['Псифистика'] * 0.1
                                       - abs(permissions['Элафристика']
                                             - permissions['Катифристика']) * 0.1)) ** 1.2, 0)
        context['mental_health'] = mental_health

        endurance = round(15 * (points['Стамина'] * 0.5
                                + points['Колдовство'] * 0.4
                                + points['Сила'] * 0.2
                                + points['Ловкость'] * 0.4
                                + (permissions['Гематомантия'] * 0.1
                                   )) ** 1.2, 0)
        context['endurance'] = endurance

        mana = round(15 * (points['Колдовство'] * 0.5
                           + points['Интеллект'] * 0.4
                           + points['Вера'] * 0.2
                           + permissions['Псифистика'] * 0.1
                           + abs(permissions['Элафристика']
                                 - permissions['Катифристика'])) ** 1.2, 0)
        context['mana'] = mana

        hungry = round(5 * (points['Сила'] * 0.3
                            + points['Ловкость'] * 0.3
                            + points['Стамина'] * 0.3
                            ) ** 1.05, 0)
        context['hungry'] = hungry

        intoxication = round(5 * (points['Сила'] * 0.7
                                  + points['Ловкость'] * 0.1
                                  + points['Стамина'] * 0.1
                                  + permissions['Гематомантия'] * 0.1
                                  ) ** 1.05, 0)
        context['intoxication'] = intoxication

        load_capacity = round(5 * (points['Стамина'] * 0.4
                                   + points['Сила'] * 0.5
                                   + points['Ловкость'] * 0.2
                                   ) ** 1.05, 0)
        context['load_capacity'] = load_capacity

        context['main_points'] = max(points, key=points.get)
        context['main_permission'] = max(permissions, key=permissions.get)
        context['avg_magic_resistance'] = round((resistances.get('Устойчивость к огню') +
                                                 resistances.get('Устойчивость к воде') +
                                                 resistances.get('Устойчивость к воздуху') +
                                                 resistances.get('Устойчивость к земле') +
                                                 resistances.get('Устойчивость к молниям') +
                                                 resistances.get('Устойчивость к свету') +
                                                 resistances.get('Устойчивость ко тьме')
                                                 ) / 7, 0)
        context['avg_physic_resistance'] = round((resistances.get('Устойчивость к дроблению') +
                                                  resistances.get('Устойчивость к порезам') +
                                                  resistances.get('Устойчивость к протыканию')
                                                  ) / 3, 0)
        # context['rov'] = rov
        # context['fov'] = fov
        # context['person_img'] = person_img
        return context


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
        except:
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
            start_points[slovar.dict_points_start.get(key)] = value

        finish_points = dict()
        for key, value in context['race_detail'].finish_points.items():
            finish_points[slovar.dict_points_max.get(key)] = value

        start_permissions = dict()
        for key, value in context['race_detail'].start_permissions.items():
            start_permissions[slovar.dict_permissions_start.get(key)] = value

        start_resistances = dict()
        for key, value in context['race_detail'].start_resistances.items():
            start_resistances[slovar.dict_resistances_start.get(key)] = value

        equipment = dict()
        for key, value in context['race_detail'].equipment.items():
            equipment[slovar.dict_equipment_start.get(key)] = value

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
        for item in context['person_bar_detail'].unallocated_points:
            context[item[0]] = item
        for item in context['person_bar_detail'].unallocated_permissions:
            context[item[0]] = item
        return context


class ActionDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр детальной информации по команде
    """
    template_name = 'poll/action/action_detail.html'
    context_object_name = 'action_detail'
    model = Action
    #queryset = Action.objects.all()
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
    # fields = ['action_name', 'action_alias', 'action_description', 'points', 'SP', 'MP', 'IP', 'PP', 'AP', 'FP',
    #           'LP', 'CP', 'BP', 'resistances', 'fire_res', 'water_res', 'wind_res', 'dirt_res', 'lightning_res',
    #           'holy_res', 'curse_res', 'crush_res', 'cut_res', 'stab_res', 'permissions', 'Fire_access',
    #           'Water_access', 'Wind_access', 'Dirt_access', 'Lightning_access', 'Holy_access', 'Curse_access',
    #           'Bleed_access', 'Nature_access', 'Mental_access', 'Twohanded_access', 'Polearm_access',
    #           'Onehanded_access',
    #           'Stabbing_access', 'Cutting_access', 'Crushing_access', 'Small_arms_access', 'Shields_access',
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

        self.cleaned_data.update({'action_name': cleaned_data.get('action_name'),
                                  'action_alias': cleaned_data.get('action_alias'),
                                  'action_description': cleaned_data.get('action_description')})

        action_points = dict()
        for key in slovar.dict_points.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            action_points[key] = self.cleaned_data[key]
        print(action_points)
        self.cleaned_data.update({'points': action_points})
        action_permissions = dict()
        for key in slovar.dict_permissions.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            action_permissions[key] = self.cleaned_data[key]
        self.cleaned_data["permissions"] = action_permissions
        action_resistances = dict()
        for key in slovar.dict_resistances.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            action_resistances[key] = self.cleaned_data[key]
        self.cleaned_data["resistances"] = action_resistances
        action_equipment = dict()
        for key in slovar.dict_equipment.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            action_equipment[key] = self.cleaned_data[key]
        self.cleaned_data.update({"equipment": action_equipment})
        action = Action.objects.get(id=pk)
        action.points.set(action_points)
        action.equipment.set(action_equipment)
        action.resistances.set(action_resistances)
        action.permissions.set(action_permissions)
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
    model = Location
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


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


        return context


class FeaturesListView(LoginRequiredMixin, ListView):
    """
    Просмотр полного списка Свойств
    """
    template_name = 'poll/feature/features_list.html'
    context_object_name = 'features_list'
    model = Feature
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
        feature = get_object_or_404(Action, pk=pk)
        if request.method == "POST":
            f = FeatureUpdateForm(self.request.POST, instance=feature)
            if f.is_valid():
                f.save()
                messages.add_message(request, messages.INFO, 'Feature updated.')
                return redirect(reverse('action_update', args=[feature.id]))
            # if request is GET the show unbound form to the user, along with data
        else:
            f = ActionUpdateForm(instance=feature)
        return render(request, 'poll/action_update.html', {'form': f, 'action': feature})

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
    Создание нового Действия
    """
    context_object_name = 'feature_add'
    queryset = Feature.objects.all()
    template_name = 'add/feature_form.html'
    login_url = 'poll:login'
    fields ='__all__'
    # fields = ['feature_name', 'feature_description', 'points', 'SP', 'MP', 'IP', 'PP', 'AP', 'FP',
    #           'LP', 'CP', 'BP', 'resistances', 'fire_res', 'water_res', 'wind_res', 'dirt_res', 'lightning_res',
    #           'holy_res', 'curse_res', 'crush_res', 'cut_res', 'stab_res', 'permissions', 'Fire_access',
    #           'Water_access', 'Wind_access', 'Dirt_access', 'Lightning_access', 'Holy_access', 'Curse_access',
    #           'Bleed_access', 'Nature_access', 'Mental_access', 'Twohanded_access', 'Polearm_access',
    #           'Onehanded_access', 'Stabbing_access', 'Cutting_access', 'Crushing_access', 'Small_arms_access',
    #           'Shields_access', 'equipment', 'helmet_status', 'chest_status', 'shoes_status', 'gloves_status',
    #           'item_status', rov, fov]

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

        self.cleaned_data.update({'feature_name': cleaned_data.get('feature_name'),

                                  'feature_description': cleaned_data.get('feature_description')})

        points = dict()
        for key in slovar.dict_points.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            points[key] = self.cleaned_data[key]

        self.cleaned_data.update({'points': points})
        permissions = dict()
        for key in slovar.dict_permissions.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            permissions[key] = self.cleaned_data[key]
        self.cleaned_data["permissions"] = permissions
        resistances = dict()
        for key in slovar.dict_resistances.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            resistances[key] = self.cleaned_data[key]
        self.cleaned_data["resistances"] = resistances
        equipment = dict()
        for key in slovar.dict_equipment.keys():
            self.cleaned_data.update({key: cleaned_data.get(key)})
            equipment[key] = self.cleaned_data[key]
        self.cleaned_data.update({"equipment": equipment})
        feature = Feature.objects.get(id=pk)
        feature.points.set(points)
        feature.equipment.set(equipment)
        feature.resistances.set(resistances)
        feature.permissions.set(permissions)
        feature.save()

        if self.request.method == "POST":
            f = FeatureCreateView(self.request.POST, instance=feature)
            if f.is_valid():
                f.save()
                messages.add_message(self.request, messages.INFO, 'Feature updated.')
                return redirect(reverse('feature_update', args=[feature.id]))

            # if request is GET the show unbound form to the user, along with data
        else:
            f = FeatureUpdateForm(instance=feature)

        return render(self.request, 'poll/feature_update.html', {'form': f, 'feature': feature})

        return self.cleaned_data

    def form_valid(self, form):
        """
        Сведения о том, кем была создана связь
        :param form:
        :return:
        """

        return super().form_valid(form)


#  REST API


class OwnerViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    model = Owner
    serializer_class = OwnerSerializer


class PersonViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    model = Person
    serializer_class = PersonSerializer


class GroupViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    model = Group
    serializer_class = GroupSerializer


class MembershipViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    model = Membership
    serializer_class = MembershipSerializer


class RaceViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    model = Race
    serializer_class = RaceSerializer
