
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
    # if dictionary == 'dict_points':
    #     return slovar.dict_points.get(res)
    # elif dictionary == 'dict_permissions':
    #     return slovar.dict_permissions.get(res)
    # elif dictionary == 'dict_resistances':
    #     return slovar.dict_resistances.get(res)
    # elif dictionary == 'dict_equipment':
    #     return slovar.dict_equipment.get(res)
    # elif dictionary == 'dict_points_start':
    #     return slovar.dict_points_start.get(res)
    # elif dictionary == 'dict_points_max':
    #     return slovar.dict_points_max.get(res)
    # elif dictionary == 'dict_permissions_start':
    #     return slovar.dict_permissions_start.get(res)
    # elif dictionary == 'dict_resistances_start':
    #     return slovar.dict_resistances_start.get(res)
    # elif dictionary == 'dict_equipment_start':
    #     return slovar.dict_equipment_start.get(res)



@register.simple_tag
def get_label(dictionary, key):
    """
    Возвращает лейбл, соответсвующий ключу словаря
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


@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data.get(key)

