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







