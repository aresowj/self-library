import os
from django import template

register = template.Library()


@register.filter
def get_file_name(file_object):
    return os.path.basename(file_object.file.name)


@register.filter
def get_dict_value(dictionary, key):
    try:
        value = dictionary.get(key)
    except KeyError:
        value = ''
    return value


@register.filter
def get_attr(obj, attr):
    return getattr(obj, attr)


@register.filter
def get_form_field(form, name):
    return form[name]


@register.filter
def true_or_false(value):
    # the value from database is unicode type in default
    value = str(value)
    if value is True or value == 'True':
        return True
    elif value is False or value == 'False':
        return False


@register.filter
def verbose_name(instance, field_name):
    return instance._meta.get_field(field_name).verbose_name.title()
