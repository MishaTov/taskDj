import uuid
from os.path import splitext

from django import template

register = template.Library()


@register.filter(name='int_')
def int_(value):
    return int(value)


@register.filter(name='get_')
def get_(dict_: dict, key):
    return dict_.get(key)


@register.filter(name='get_filename')
def get_filename(filepath):
    filepath, ext = splitext(str(filepath))
    filename = filepath.split('/')[-1][:-39] + ext
    return filename
