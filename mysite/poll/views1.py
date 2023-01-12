from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from . import slovar
from .serializers import *


class PersonDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр стартовой информации по персонажу
    """
    template_name = 'poll/person/person_detail.html'
    context_object_name = 'person_detail'
    model = Person
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        points = {i: 0 for i in slovar.dict_points}
        permissions = {i: 0 for i in slovar.dict_permissions}
        resistances = {i: 0 for i in slovar.dict_resistances}
        equipment = {i: 0 for i in slovar.dict_equipment}
        conditions = {i: 0 for i in slovar.dict_conditions}
        level = 0
        unallocated_points = 6
        unallocated_permissions = 3

        # Проверяем, есть ли записи в PersonBar
        if not self.object.personbar_set.all().exists():
            # записей  в Personbar нет - нужно проверить, есть ли записи в History
            history_persons = self.object.history_set.all()
            # history_persons = self.history_set.all()
            if history_persons.exists():
                # если есть - нужно взять последнюю и скопировать в person_bar
                last = history_persons.latest('last_update')
                points = last.points_new
                permissions = last.permissions_new
                resistances = last.resistances_new
                equipment = last.equipment_new
                unallocated_points = last.un_points_new
                unallocated_permissions = last.un_permissions_new
                fov = last.fov_new
                rov = last.rov_new
                level = last.level_new
                conditions = last.conditions_new

                obj = PersonBar(person=self.object, race=self.object.race, summary_points=points,
                                summary_permissions=permissions, summary_resistances=resistances,
                                summary_equipment=equipment, unallocated_points=unallocated_points,
                                unallocated_permissions=unallocated_permissions,
                                fov=fov, rov=rov, level=level, conditions=conditions)
                obj.save()  # скопировали

            else:
                # если нет ни в person_bar, ни в history - нужно добавить первую запись из рас и слабостей
                # берем инфу из расы и добавляем к особенностям
                info = self.object.race

                for key, value in info.start_points.items():
                    points[key] = value

                for key, value in info.start_permissions.items():
                    permissions[key] = value

                for key, value in info.start_resistances.items():
                    resistances[key] = value

                for key, value in info.equipment.items():
                    equipment[key] = value

                fov = info.fov
                rov = info.rov

                person_features = self.object.features.all()  # получим Список фич
                if not person_features.exists():
                    context['features'] = ['без особенностей']
                else:
                    # Считаем добавки по всем статистикам из-за особенностей

                    for feature in person_features:

                        for key in points.keys():
                            points[key] += feature.points[key]

                        for key in permissions.keys():
                            permissions[key] += feature.permissions[key]

                        for key in resistances.keys():
                            resistances[key] = feature.resistances[key]

                        for key in equipment.keys():
                            equipment[key] = feature.equipment[key]

                    # На основании расы и особенностей считаем кондиции.
                    conditions["health"] = round(25 * (points['sp'] * 0.2
                                                       + points['ip'] * 0.2
                                                       + points['pp'] * 0.5
                                                       + points['ap'] * 0.4
                                                       + points['bp'] * 0.4
                                                       + (permissions['bleed_access'] * 0.1
                                                          + permissions['nature_access'] * 0.1
                                                          + permissions['mental_access'] * 0.1)) ** 1.5, 0)

                    conditions["mental_health"] = round(10 * (points['ip'] * 0.4
                                                              + points['fp'] * 0.3
                                                              + points['bp'] * 0.5
                                                              + (permissions['mental_access'] * 0.1
                                                                 - abs(permissions['holy_access']
                                                                       - permissions['curse_access']) * 0.1)) ** 1.2, 0)

                    conditions["endurance"] = round(15 * (points['sp'] * 0.5
                                                          + points['mp'] * 0.4
                                                          + points['pp'] * 0.2
                                                          + points['ap'] * 0.4
                                                          + (permissions['bleed_access'] * 0.1
                                                             )) ** 1.2, 0)

                    conditions["mana"] = round(15 * (points['mp'] * 0.5
                                                     + points['ip'] * 0.4
                                                     + points['fp'] * 0.2
                                                     + permissions['mental_access'] * 0.1
                                                     + abs(permissions['holy_access']
                                                           - permissions['curse_access'])) ** 1.2, 0)

                    conditions["hungry"] = round(5 * (points['pp'] * 0.3
                                                      + points['ap'] * 0.3
                                                      + points['sp'] * 0.3
                                                      ) ** 1.05, 0)

                    conditions["intoxication"] = round(5 * (points['pp'] * 0.7
                                                            + points['ap'] * 0.1
                                                            + points['sp'] * 0.1
                                                            + permissions['bleed_access'] * 0.1
                                                            ) ** 1.05, 0)

                    conditions["load_capacity"] = round(5 * (points['sp'] * 0.4
                                                             + points['pp'] * 0.5
                                                             + points['ap'] * 0.2
                                                             ) ** 1.05, 0)
                    conditions["avg_magic_resistance"] = round((resistances.get('fire_res') +
                                                                resistances.get('water_res') +
                                                                resistances.get('wind_res') +
                                                                resistances.get('dirt_res') +
                                                                resistances.get('lightning_res') +
                                                                resistances.get('holy_res') +
                                                                resistances.get('curse_res')
                                                                ) / 7, 0)
                    conditions["avg_physic_resistance"] = round((resistances.get('crush_res') +
                                                                 resistances.get('cut_res') +
                                                                 resistances.get('stab_res')
                                                                 ) / 3, 0)

                    # Запишем 1-ю запись по Персонажу в PersonBar. для этого сконвертируем в sp,mp вместо стамины
                    info = PersonBar(person=self.object, race=self.object.race, summary_points=points,
                                     summary_permissions=permissions,
                                     summary_resistances=resistances,
                                     summary_equipment=equipment, unallocated_points=6,
                                     unallocated_permissions=3,
                                     fov=fov, rov=rov, level=0, conditions=conditions)
                    info.save()

        else:
            #  Записи есть. Значит, не нужно лазать в слабости и особенности
            # Для расчета текущих статистик берем информацию из PersonBar. Там только 1 запись, остальное в логе

            info = self.object.personbar_set.all()[0]
            for key, value in info.summary_points.items():
                points[key] = value

            for key, value in info.summary_permissions.items():
                permissions[key] = value

            for key, value in info.summary_resistances.items():
                resistances[key] = value

            for key, value in info.summary_equipment.items():
                equipment[key] = value
            fov = info.fov
            rov = info.rov
            level = info.level
            unallocated_points = info.unallocated_points
            unallocated_permissions = info.unallocated_permissions

        # про членство в группе
        person_group = self.object.group_set.all()  # queryset из одной группы, т.к одновременно только в 1 группе можно
        if person_group.exists():  # состоит  в группе - или Inviter, или просто участник
            members = person_group[0].members.all()  # Прочие участники группы, кроме нашего Person
            context['group_status'] = 'в группе'
            context['inviter_person'] = \
                person_group[0].members.through.objects.filter(group__id=person_group[0].pk)[0].inviter
            context['participants'] = members

        else:
            context['group_status'] = 'не в группе'

        for key, value in conditions.items():
            context[key] = value

        context['main_point'] = max(points, key=points.get)
        context['main_permission'] = max(permissions, key=permissions.get)
        context['level'] = level
        context['rov'] = rov
        context['fov'] = fov
        context['conditions'] = conditions
        context['status_'] = ['Свободен' if context['person_detail'].status == 1
                              else 'Занят' if context['person_detail'].status == 2 else 'Заморозка'][0]
        context['person_detail'].status_ = ['Свободен' if context['person_detail'].status == 1
                                            else 'Занят' if context['person_detail'].status == 2 else 'Заморозка'][0]
        context['summary_points'] = points
        context['summary_permissions'] = permissions
        context['summary_resistances'] = resistances
        context['summary_equipment'] = equipment
        context['unallocated_points'] = unallocated_points
        context['unallocated_permissions'] = unallocated_permissions
        context['features'] = self.object.features
        context['personbar_detail'] = self.object.personbar_set.all()
        context['inventory_detail'] = self.object.inventory_set.all()
        context['safe_detail'] = self.object.safe_set.all()
        context['thing_detail'] = self.object.thing_set.all()
        context['consumable_detail'] = self.object.consumable_set.all()
        context['money_detail'] = self.object.money_set.all()
        # context['person_img'] = person_img
        return context


class PersonBarDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр текущей информации - кондиций, характеристик, навыков, сопротивлений, снаряжения по Персонажу
    Текущие статистики - сумма по race, feature, consumable, thing, spell, а также с учетом level (из Person)
    После какого-либо action их значение изменится и будет помещено в PersonBar
    Старое значение будет перемещено в history
    """
    template_name = 'poll/personbar/personbar_detail.html'
    context_object_name = 'personbar_detail'
    model = PersonBar
    login_url = 'poll:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person'] = self.object.person
        points = {i: 0 for i in slovar.dict_points}
        permissions = {i: 0 for i in slovar.dict_permissions}
        resistances = {i: 0 for i in slovar.dict_resistances}
        equipment = {i: 0 for i in slovar.dict_equipment}
        conditions = {i: 0 for i in slovar.dict_conditions}
        unallocated_points = 6
        unallocated_permissions = 3

        for key, value in self.object.summary_points.items():
            points[key] = value

        for key, value in self.object.summary_permissions.items():
            permissions[key] = value

        for key, value in self.object.summary_resistances.items():
            resistances[key] = value

        for key, value in self.object.summary_equipment.items():
            equipment[key] = value

        for key, value in self.object.conditions.items():
            conditions[key] = value

        fov = self.object.fov
        rov = self.object.rov
        level = self.object.level
        unallocated_points = self.object.unallocated_points
        unallocated_permissions = self.object.unallocated_permissions

        context['level'] = level
        context['rov'] = rov
        context['fov'] = fov
        context['conditions'] = conditions
        context['summary_points'] = points
        context['summary_permissions'] = permissions
        context['summary_resistances'] = resistances
        context['summary_equipment'] = equipment
        context['unallocated_points'] = unallocated_points
        context['unallocated_permissions'] = unallocated_permissions
        for key, value in conditions.items():
            context[key] = value
        # context['color'] = {"health": 'bg-danger', "mental_health": 'bg-info', "endurance": 'bg_success',
        #                     "mana": 'bg-primary', "hungry": 'bg-secondary', "intoxication": 'bg-warning',
        #                     "load_capacity": 'bg-dark', "avg_magic_resistance": 'bg-success bg-opacity-25',
        #                     "avg_physic_resistance":'bg-primary bg-opacity-25'}

        return context


class PersonBarsListView(LoginRequiredMixin, ListView):
    """
    Просмотр списка групп Персонажей
    """
    template_name = 'poll/personbar/personbars_list.html'
    context_object_name = 'personbars_list'
    model = PersonBar
    login_url = 'poll:login'
