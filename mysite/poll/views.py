from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout  # add this
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Owner, Person, Group, Membership, Race
from .serializers import OwnerSerializer, PersonSerializer, GroupSerializer, MembershipSerializer, RaceSerializer
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import NewUserForm
from django.http import JsonResponse


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


# Это просто для примера
# class RegisterFormView(FormView):
#     template_name = 'contact.html'
#     form_class = RegisterForm
#     # success_url = '/thanks/'
#
#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         form.send_email()
#         return super().form_valid(form)


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
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("poll:index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="poll/login.html", context={"login_form": form})


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
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="poll/password/password_reset.html",
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


class OwnerCreateView(JsonableResponseMixin, CreateView):
    """
    Добавление нового игрока
    """
    model = Owner
    fields = ['owner_name', 'owner_description', 'link']

    def form_valid(self, form):
        """
        Сведения о том, кем был создан игрок
        :param form:
        :return:
        """
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def add_owner(owner_name, owner_description, link):
        """
        Добавление нового игрока в список
        :param owner_name:
        :param owner_description:
        :param link:
        :return:
        """
        try:
            Owner.objects.get(owner_name=owner_name)
            response = 'Игрок %s уже существует'
        except ObjectDoesNotExist:
            b = Owner(owner_name=owner_name, owner_description=owner_description, link=link)
            b.save()
            response = 'Игрок %s добавлен'
        finally:
            return HttpResponse(response)


class OwnerUpdateView(UpdateView):
    """
    Редактирование данных игрока
    """
    model = Owner
    fields = ['owner_name', 'owner_description', 'link']
    template_name_suffix = '_update'

    def form_valid(self, form):
        """
        Сведения о том, кем был изменен игрок
        :param form:
        :return:
        """
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class OwnerDeleteView(DeleteView):
    """
    Удаление игрока
    """
    #  model = Owner
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll:owners-list')
    context_object_name = 'owner_detail'
    queryset = Owner.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner_name'] = context['owner_detail'].owner_name
        return context


class OwnerDetailView(DetailView):
    """
    Просмотр детальной информации по игроку
    """
    template_name = 'poll/owner/owner_detail.html'
    context_object_name = 'owner_detail'
    queryset = Owner.objects.all()

    # def get_queryset(request, self):
    #     """
    #     Просмотр детальной информации по владельцу указанного персонажа
    #     """
    #     selected_person = get_object_or_404(Person, person_name=self.kwargs['person_name'])
    #     context = {'owner_detail': selected_person.owner}
    #     return render(request, 'poll/owner/owner_detail.html', context)
    #
    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object(queryset=Owner.objects.all())
    #     return super().get(request, *args, **kwargs)
    #

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner_status_'] = ['Занят' if context['owner_detail'].owner_status == '1' else 'Свободен'][0]
        return context
    #
    # def get_queryset(self):
    #     return self.object.person_set.all()


class OwnersListView(ListView):
    """
    Просмотр полного списка игроков
    """
    template_name = 'poll/owner/owners_list.html'
    context_object_name = 'owners_list'
    queryset = Owner.objects.all()


class OwnersFreeListView(ListView):
    """
    Просмотр  списка свободных игроков
    """
    template_name = 'poll/free_owner/free_owners_list.html'
    context_object_name = 'free_owners_list'
    queryset = Owner.objects.filter(person__status=1).distinct('owner_name')



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


class PersonCreateView(JsonableResponseMixin, CreateView):
    """
    Добавление нового персонажа
    """
    model = Person
    fields = ['person_name', 'owner', 'link', 'biography', 'character', 'interests', 'phobias', 'race',
              'location_birth', 'birth_date', 'location_death', 'death_date', 'status']


    def form_valid(self, form):
        """
        Сведения о том, кем был создан персонаж
        :param form:
        :return:
                """
        form.instance.created_by = self.request.user
        return super().form_valid(form)




class PersonUpdateView(UpdateView):
    """
    Редактирование персонажа
    """
    model = Person

    fields = ['person_name', 'owner', 'link', 'biography', 'character', 'interests', 'phobias', 'race',
              'location_birth', 'birth_date', 'location_death', 'death_date', 'status']

    template_name_suffix = '_update'

    def form_valid(self, form):
        """
        Сведения о том, кем был изменен персонаж
        :param form:
        :return:
                """
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class PersonDeleteView(DeleteView):
    """
    Удаление персонажа
    """
    # model = Person
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll:persons-list')
    context_object_name = 'person_detail'
    queryset = Person.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person_name'] = context['person_detail'].person_name
        return context



class PersonsFreeListView(ListView):
    """
    Просмотр  списка свободных персонажей
    """
    template_name = 'poll/free_person/free_persons_list.html'

    context_object_name = 'free_persons_list'
    queryset = Person.objects.filter(status=1)


class PersonsBusyListView(ListView):
    """
    Просмотр  списка занятых персонажей
    """
    template_name = 'poll/busy_person/busy_persons_list.html'
    context_object_name = 'busy_persons_list'
    queryset = Person.objects.filter(status=0)


class PersonsFreezListView(ListView):
    """
    Просмотр  списка заморозки персонажей
    """
    template_name = 'poll/freez_person/freez_persons_list.html'
    context_object_name = 'freez_persons_list'
    queryset = Person.objects.filter(status=2)


class PersonsListView(ListView):
    """
    Занятые персонажи: status= 0
    Свободные персонажи: status = 1
    Заморозка : status = 2
    :param status:
    :return:
    """
    template_name = 'poll/person/persons_list.html'
    context_object_name = 'persons_list'
    queryset = Person.objects.all()


class PersonDetailView(DetailView):
    """
    Просмотр информации по персонажу
    """
    template_name = 'poll/person/person_detail.html'
    context_object_name = 'person_detail'
    queryset = Person.objects.all()


    # model = Person

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_'] = ['Занят' if context['person_detail'].status == 1 else 'Заморозка' if context['person_detail'].status == 2 else 'Свободен'][0]
        #person_groups = Person.objects.get(id=context['person_detail'].pk).group_set.all()

        # Person может быть inviter, участник группы или никто

        # Если не inviter, но участник группы - >= 1 (число людей в группе), иначе 0
        if Membership.objects.filter(person=Person.objects.get(id=context['person_detail'].pk).id).count() > 0:
            context['group_status'] = 'в группе'
            person_groups = Membership.objects.filter(
                person=Person.objects.get(id=context['person_detail'].pk).id)
            context['inviter_person'] = person_groups[0].inviter
            context['participants'] = person_groups
            # Если не inviter или не состоит в группе - получится 0
        elif Membership.objects.filter(inviter=Person.objects.get(id=context['person_detail'].pk).id).count() == 0:
            context['group_status'] = 'не в группе'
        else:
            # Если inviter - >=1 ( число людей в группе
            context['group_status'] = 'в группе'
            person_groups = Membership.objects.filter(
                inviter=Person.objects.get(id=context['person_detail'].pk).id)
            context['inviter_person'] = person_groups[0].inviter
            context['participants'] = person_groups
            #contex['group_status'] = 'в группе'
        return context


class GroupDetailView(DetailView):
    """
    Просмотр информации по конкретной группе
    """
    template_name = 'poll/group/group_detail.html'
    context_object_name = 'group_detail'

    queryset = Group.objects.all()


def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    members = self.members.through.objects.filter(group__id=self.id)
    context['members'] = members
    context['inviter_person'] = members[0].inviter
    return context


class GroupsListView(ListView):
    """
    Просмотр списка групп Персонажей
    """
    template_name = 'poll/group/groups_list.html'
    context_object_name = 'groups_list'
    queryset = Group.objects.all()


class GroupCreateView(JsonableResponseMixin, CreateView):
    """
    Создание новой группы
    """
    model = Group
    fields = ['group_name', 'members']

    def form_valid(self, form):
        """
        Сведения о том, кем была создана группа
        :param form:
        :return:
        """
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class GroupUpdateView(UpdateView):
    """
    Редактирование группы
    """
    model = Group

    fields = ['group_name', 'members']
    template_name_suffix = '_update'

    def form_valid(self, form):
        """
        Сведения о том, кем была изменена группа
        :param form:
        :return:
        """
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class GroupDeleteView(DeleteView):
    """
    Удаление группы
    """
    # model = Group
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll:groups-list')
    context_object_name = 'group_detail'
    queryset = Group.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group_name'] = context['group_detail'].group_name
        return context


class MembershipListView(ListView):
    """
    Просмотр списка связей
    """
    template_name = 'poll/membership/members_list.html'
    context_object_name = 'members_list'
    queryset = Membership.objects.all()


class MembershipDetailView(DetailView):
    """
    Просмотр информации по конкретному виду связи
    """
    template_name = 'poll/membership/membership_detail.html'
    context_object_name = 'membership_detail'
    queryset = Membership.objects.all()
    #  model = Membership


class MembershipCreateView(JsonableResponseMixin, CreateView):
    """
    Создание новой связи
    """
    model = Membership
    fields = ['group', 'person', 'inviter', 'invite_reason']


    def form_valid(self, form):
        """
        Сведения о том, кем была создана связь
        :param form:
        :return:
        """
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class MembershipUpdateView(UpdateView):
    """
    Редактирование группы
    """
    model = Membership

    fields = ['group', 'person', 'inviter', 'invite_reason']
    template_name_suffix = '_update'

    def form_valid(self, form):
        """
        Сведения о том, кем была изменена связь
        :param form:
        :return:
        """
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class MembershipDeleteView(DeleteView):
    """
    Удаление связи
    """
    # model = Membership
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll:membership-list')
    context_object_name = 'membership_detail'
    queryset = Membership.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group_name'] = context['membership_detail'].group.group_name
        context['person_name'] = context['membership_detail'].person.person_name
        context['inviter'] = context['membership_detail'].person.membership_invites
        return context


class RacesListView(ListView):
    """
    Просмотр полного списка Рас
    """
    template_name = 'poll/race/races_list.html'
    context_object_name = 'races_list'
    queryset = Race.objects.all()


class RaceCreateView(JsonableResponseMixin, CreateView):
    """
    Создание новой Расы
    """
    model = Race
    fields = ['race_name', 'race_description', 'lifetime', 'start_points', 'finish_points',
              'start_resistanses', 'start_permissions', 'equipment']

    def form_valid(self, form):
        """
        Сведения о том, кем была создана связь
        :param form:
        :return:
        """
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class RaceUpdateView(UpdateView):
    """
    Редактирование Расы
    """
    model = Race

    fields = ['race_name', 'race_description', 'lifetime', 'start_points', 'finish_points',
              'start_resistanses', 'start_permissions', 'equipment']
    template_name_suffix = '_update'

    def form_valid(self, form):
        """
        Сведения о том, кем была изменена связь
        :param form:
        :return:
        """
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class RaceDeleteView(DeleteView):
    """
    Удаление Расы
    """
    # model = Race
    template_name_suffix = '_delete'
    success_url = reverse_lazy('poll:race-list')
    context_object_name = 'race_detail'
    queryset = Race.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['race_name'] = context['race_detail'].race_name
        return context


class RaceDetailView(DetailView):
    """
    Просмотр детальной информации по расе
    """
    template_name = 'poll/race/race_detail.html'
    context_object_name = 'race_detail'
    queryset = Race.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for item in context['race_detail'].finish_points:
            context[item[0]] = item
        for item in context['race_detail'].finish_points:
            context[item[0]] = item
        for item in context['race_detail'].start_resistanses:
            context[item[0]] = item
        for item in context['race_detail'].start_permissions:
            context[item[0]] = item
        for item in context['race_detail'].equipment:
            context[item[0]] = item

        return context

#  REST API


class OwnerViewSet(viewsets.ModelViewSet):
    # model = Owner
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class PersonViewSet(viewsets.ModelViewSet):
    # model = Person
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class GroupViewSet(viewsets.ModelViewSet):
    # model = Group
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class MembershipViewSet(viewsets.ModelViewSet):
    # model = Membership
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


class RaceViewSet(viewsets.ModelViewSet):
    # model = Race
    queryset = Race.objects.all()
    serializer_class = RaceSerializer
