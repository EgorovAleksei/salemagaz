from django import template

from main.utils import get_menu_cat

register = template.Library()


@register.simple_tag()
def menu_cat():
    return get_menu_cat()
