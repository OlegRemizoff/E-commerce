from django import template
from main.models import Category

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.get_category_for_navbar()