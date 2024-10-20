import random

from django.utils.http import urlencode
from goods.models import Products
from django import template
from django.db.models import Max
from main.utils import get_menu_cat

register = template.Library()


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context["request"].GET.dict()
    query.update(kwargs)
    return urlencode(query)


@register.simple_tag
def top_products():

    max_id = Products.objects.aggregate(Max("id"))["id__max"]
    p1 = random.randint(0, max_id)

    products = Products.objects.filter(pk__gte=p1 + 1000, pk__lte=p1 + 10000)[:3]
    return products
    # return {"products": products}
