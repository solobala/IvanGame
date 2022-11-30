from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.http import HttpResponse
from django.template import loader
from rest_framework import generics

from .models import Owner, Person, RelationType, PersonToPersonAction
from .serializers import OwnerSerializer, PersonSerializer, RelationTypeSerializer, PersonToPersonActionSerializer


def index(request):
    # Это должна быть стартовая страница с картинками,
    # ссылкой на регистрацию в игре, формой для входа зарегистрированных
    context = {'game': "Ivan's Game, Hello"}
    return render(request, 'poll/index.html', context)


def get_owners_list(request):
    """
    Общий список игроков
    :return:
    """
    # response = "Список игроков %s."
    # template = loader.get_template('poll/owners_list.html')
    owners_list = Owner.objects.all()
    context = {
        'owners_list': owners_list,
    }
    return render(request, 'poll/owners_list.html', context)
    # return HttpResponse(template.render(context, request))
    # output = ', '.join([q.owner_name for q in owners_list])
    # return HttpResponse(response % output)


def get_persons_list(request):
    """
    Общий список персонажей в виде строки через ,
    :return:
    """
    # response = "Список персонажей %s."
    persons_list = Person.objects.all()
    context = {
        'persons_list': persons_list,
    }
    return render(request, 'poll/persons_list.html', context)
    # output = ', '.join([q.person_name for q in persons_list])
    # return HttpResponse(response % output)


def find_persons_by_owner(request, owner_name):
    """
    Список персонажей игрока owner_name в виде строки через ,
    :param request:
    :param owner_name:
    :return:
    """
    try:
        selected_owner = Owner.objects.get(owner_name=owner_name)
        # selected_owner = Owner.objects.get(owner_name__icontains=owner_name) # выдает похожих, но если >1 - ошибка
        persons_by_owner_list = selected_owner.person_set.all()
        context = {
            'persons_by_owner_list': persons_by_owner_list,
        }

        # output = ', '.join([q.person_name for q in persons_by_owner_list])
        # response = "Персонажи игрока %s."
    except ObjectDoesNotExist:
        raise Http404("Игрок %s не найден")
    finally:
        # return HttpResponse(response % output)
        return render(request, 'poll/persons_by_owner_list.html', context)

def find_owner_by_person(request, person_name):
    """
    Игрок ищется по person_name персонажа
    :param request:
    :param person_name:
    :return:
    """
    try:
        selected_person = Person.objects.get(person_name=person_name)
        owner_name = selected_person.owner.owner_name
        response = "Владелец персонажа %s."
    except ObjectDoesNotExist:
        raise Http404("Персонаж %s не найден")
    finally:
        return HttpResponse(response % owner_name)


def get_all_participants(request, person_name):
    """
    Список всех участников группы, в которой состоит
    персонаж person_name
    :param request:
    :param person_name:
    :return:
    """
    try:
        selected_person = Person.objects.get(person_name=person_name)
        persons_by_group_list = PersonToPersonAction.objects.filter(person_id=selected_person.id)
        output = ', '.join([q.other_person.person_name for q in persons_by_group_list])
        response = "Участники группы %s."
    except ObjectDoesNotExist:
        raise Http404("Персонаж %s не найден")
    finally:
        return HttpResponse(response % output)


def get_selected_persons_list(status_id):
    """
    Занятые персонажи: status_id = 0
    Свободные персонажи: status_id = 1
    Заморозка : status_id = 2
    :param status_id:
    :return:
    """
    response = "Список выбранных персонажей %s."
    persons_list = Person.objects.filter(status_id=status_id)
    output = ', '.join([q.person_name for q in persons_list])
    return HttpResponse(response % output)


def get_free_owner_list():
    """
    Список свободных игроков
    определяется по наличию свободного персонажа
    со статусом status_id = 1
    :return:
    """
    response = "Список свободных игроков %s."
    free_persons_list = Person.objects.filter(status_id=1)
    output = ', '.join(set([q.owner.owner_name for q in free_persons_list]))
    return HttpResponse(response % output)


def add_owner_to_list(owner_name, owner_description, link):
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


def delete_owner_from_list(owner_name):
    """
    Удаление игрока и всех его персонажей из списка
    :param owner_name:
    :return:
    """
    try:
        owner = Owner.objects.get(owner_name=owner_name)
        owner.delete()
        response = 'Игрок  %s удален'
    except ObjectDoesNotExist:
        response = 'Игрок %s не найден'
    finally:
        return HttpResponse(response)


def add_person_to_list(owner_name, person_name, link, person_description, race_id, location_id_birth, birth_date,
                       status_id):
    """
    Добавление персонажа в список
    :param owner_name:
    :param person_name:
    :param link:
    :param person_description:
    :param race_id:
    :param location_id_birth:
    :param birth_date:
    :param status_id:
    :return:
    """
    try:
        owner = Owner.objects.get(owner_name=owner_name)  #  проверяем, если ли такой игрок

        try:  # проверяем, нет ли уже такого персонажа у кого-либо
            person = Person.objects.get(person_name=person_name)
            response = 'Игрок c таким ником уже существует'

        except ObjectDoesNotExist:
            person = Person(person_name=person_name, link=link, person_description=person_description, race_id=race_id,
                            location_id_birth=location_id_birth, birth_date=birth_date, status_id=status_id)
            person.owner = owner
            person.save()
            response = 'Персонаж добавлен'

    except ObjectDoesNotExist:
        response = 'Игрок не найден'

    finally:
        return HttpResponse(response)


def delete_person_from_list(person_name):
    """
    Удаление персонажа
    :param person_name:
    :return:
    """
    try:  # проверяем, есть ли персонаж в общем списке
        person = Person.objects.get(person_name=person_name)
        person.delete()
        response = 'Игрок %s удален'

    except ObjectDoesNotExist:
        response = 'Игрок %s отсутствует в списке'

    finally:
        return HttpResponse(response)


def add_person_to_group(who_added, whom_added):
    """
    Добавление персонажа в группу
    :param who_added: персонаж, которого следует добавить  вгруппу
    :param whom_added: персонаж, по которому определяется группа
    :return:
    """
    try:  # проверяем, есть ли добавляемый персонаж в общем списке персонажей
        person_who = Person.objects.get(person_name=who_added)

        try:  # проверяем, есть ли другой участник в списке
            person_whom = Person.objects.get(person_name=whom_added)
        except ObjectDoesNotExist:
            responce = 'Персонаж, в группу к которому добавляем учатника, не найден'
        finally:
            pass

    except ObjectDoesNotExist:
        responce = 'Персонаж - участник группы не найден'

    finally:
        try:  # проверяем, не состоят ли они уже в группе
            action = PersonToPersonAction.objects.get(person__in=[person_who, person_whom],
                                                      other_person__in=[person_who, person_whom])
            response = "Данные персонажи  уже являются участниками группы"

        except ObjectDoesNotExist: # данные персонажи не состоят в одной группе

            #  добавляем персонажей person_who и person_whom в группы друг к другу
            new_action_who = PersonToPersonAction(person=person_who.id, relation_type_id=1, other_person=person_whom.id)
            new_action_whom = PersonToPersonAction(person=person_whom.id, relation_type_id=1,
                                                   other_person=person_who.id)

            # добавляем person_who к другим участникам группы person_whom и наоборот
            other_participants_list = PersonToPersonAction.objects.filter(person=person_whom.id)

            for participant in other_participants_list:

                new_action_who = PersonToPersonAction(person=person_who.id, relation_type_id=1,
                                                      other_person=participant.id)
                new_action_whom = PersonToPersonAction(person=participant.id, relation_type_id=1,
                                                       other_person=person_who.id)
            response = 'Персонаж %s добавлен в группу к персонажу %s'

        finally:
            pass
    return HttpResponse(response)


def delete_person_from_group(person_name):
    """
    Удаление персонажа из группы
    :param person_name:
    :return:
    """
    try:  # проверяем, есть ли персонаж в общем списке
        person = Person.objects.get(person_name=person_name)

          # проверяем, состоит ли персонаж в группе
        actions = PersonToPersonAction.objects.filter(person=person.id)

        if len(actions)>0:

            for action in actions:
                action.delete() # удаляем все прочих участников для данного персонажа
                other_action = PersonToPersonAction.objects.get(person = action.other_person.id, other_person=person.id)
                other_action.delete() # Удаляем персонаж из группы для всех участников группы
            response = 'Игрок %s удален из группы'

        else:  # данный персонаж не состоит в  группе

            response = 'Персонаж %s не состоит в группе'

    except ObjectDoesNotExist: # Персонаж не найден
        responce = 'Персонаж  не найден'

    finally:
        return HttpResponse(response)


class OwnerAPIView(generics.ListCreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class PersonAPIView(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class RelationTypeAPIView(generics.ListCreateAPIView):
    queryset = RelationType.objects.all()
    serializer_class = RelationTypeSerializer


class PersonToPersonActionAPIView(generics.ListCreateAPIView):
    queryset = PersonToPersonAction.objects.all()
    serializer_class = PersonToPersonActionSerializer


