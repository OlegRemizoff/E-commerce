from django import template
from main.models import Category, SmartPhone, Notebook


register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.get_category_for_navbar()


@register.simple_tag()
def get_smartphones():
    return SmartPhone.objects.all()


@register.simple_tag()
def get_notebooks():
    return Notebook.objects.all()


@register.filter
def to_class_name(value):
    return value.__class__._meta.model_name


@register.inclusion_tag('inc/_header.html', takes_context=True)
def get_header(context):
    return context