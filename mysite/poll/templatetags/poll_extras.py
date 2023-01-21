import json
from django import template
from .. import slovar

register = template.Library()


@register.simple_tag
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.get_field(field_name).verbose_name.title()


@register.filter
def get_max(dictionary):
    """
    Возвращает ключ, соответствующий максимальному значению словаря
    """
    return max(dictionary, key=dictionary.get)


@register.simple_tag
def get_label(dictionary, key):
    """
    Возвращает лейбл, соответствующий ключу словаря
    имя словаря и значение ключа - строки
    """
    if dictionary == 'dict_points':
        return slovar.dict_points.get(key)
    elif dictionary == 'dict_permissions':
        return slovar.dict_permissions.get(key)
    elif dictionary == 'dict_resistances':
        return slovar.dict_resistances.get(key)
    elif dictionary == 'dict_equipment':
        return slovar.dict_equipment.get(key)
    elif dictionary == 'dict_points_start':
        return slovar.dict_points_start.get(key)
    elif dictionary == 'dict_points_max':
        return slovar.dict_points_max.get(key)
    elif dictionary == 'dict_permissions_start':
        return slovar.dict_permissions_start.get(key)
    elif dictionary == 'dict_resistances_start':
        return slovar.dict_resistances_start.get(key)
    elif dictionary == 'dict_equipment_start':
        return slovar.dict_equipment_start.get(key)
    elif dictionary == 'dict_conditions':
        return slovar.dict_conditions.get(key)
    elif dictionary == 'dict_damage':
        return slovar.dict_damage.get(key)


@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    """
    возвращает значение  из питоновского словаря по ключу
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data.get(key)


@register.filter('get_value_from_json')
def get_value_from_json(json_data, key):
    """
    возвращает значение питоновского словаря, сконвертированного из json
    usage example {{ your_json|get_value_from_json:your_key }}
    """
    if key:
        return json.loads(json_data).get(key)


@register.filter('convert_to_dict')
def convert_to_dict(json_data):
    """
    Возвращаяет питоновский словарь? crjydthnbhjdfyysq bp оыщт
    usage example {{ your_json|convert_to_dict }}
    """
    return json.loads(json_data)

@register.simple_tag
def get_keys(dictionary):
    """
    Возвращает лейбл, соответсвующий ключу словаря
    имя словаря и значение ключа - строки
    """
    if dictionary == 'dict_points':
        return slovar.dict_points.keys()
    elif dictionary == 'dict_permissions':
        return slovar.dict_permissions.keys()
    elif dictionary == 'dict_resistances':
        return slovar.dict_resistances.keys()
    elif dictionary == 'dict_equipment':
        return slovar.dict_equipment.keys()
    elif dictionary == 'dict_points_start':
        return slovar.dict_points_start.keys()
    elif dictionary == 'dict_points_max':
        return slovar.dict_points_max.keys()
    elif dictionary == 'dict_permissions_start':
        return slovar.dict_permissions_start.keys()
    elif dictionary == 'dict_resistances_start':
        return slovar.dict_resistances_start.keys()
    elif dictionary == 'dict_equipment_start':
        return slovar.dict_equipment_start.keys()
    elif dictionary == 'dict_conditions':
        return slovar.dict_conditions.keys()
    elif dictionary == 'dict_damage':
        return slovar.dict_damage.keys()