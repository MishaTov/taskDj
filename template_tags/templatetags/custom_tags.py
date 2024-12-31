from os.path import splitext

from django import template
from django.forms import BoundField
from django.http import HttpRequest

register = template.Library()


@register.filter(name='get_')
def get_(dict_: dict, key):
    return dict_.get(key)


@register.filter(name='get_filename')
def get_filename(filepath):
    filepath, ext = splitext(str(filepath))
    filename = filepath.split('/')[-1][:-39] + ext
    return filename


@register.filter(name='css_class')
def add_css_class(field: BoundField, css_class: str):
    css_classes = field.field.widget.attrs.get('class', '')
    css_classes = ' '.join(css_classes.split() + css_class.split())
    field.field.widget.attrs['class'] = css_classes
    return field


@register.simple_tag
def replace_url_param(request: HttpRequest, param, value):
    request = request.GET.copy()
    request[param] = value
    return request.urlencode()
