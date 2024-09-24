from django import template

register = template.Library()


@register.filter(name='int_')
def int_(value):
    return int(value)


@register.filter(name='get_')
def get_(dict_: dict, key):
    return dict_.get(key)
