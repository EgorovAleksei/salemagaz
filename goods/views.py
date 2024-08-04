from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render

from goods.models import Products
from goods.utils import q_search


def catalog(request, category_id=0):
    page = request.GET.get("page", 1)
    on_sale = request.GET.get("on_sale", None)
    order_by = request.GET.get("order_by", None)
    query = request.GET.get("q", None)

    if category_id:
        print(category_id)
        # goods = get_object_or_404(Products.objects.filter(category=category_id).
        #                       select_related('category', 'brand'))
        goods = Products.objects.filter(category=category_id).select_related(
            "category", "brand"
        )
    elif query:
        goods = q_search(query)
    else:
        goods = (
            Products.objects.all()
            .select_related("category", "brand")
            .order_by("-updated")
        )
    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by:
        goods = goods.order_by(order_by)

    # goods = get_list_or_404(goods)  не работает почему-то
    paginator = Paginator(goods, 15)
    current_page = paginator.page(page)

    context = {
        "title": "SaleMagaz - Товары",
        "goods": current_page,
        "category_id": category_id,
    }

    return render(request, "goods/catalog.html", context)


def product(request, product_id):
    product = Products.objects.select_related("category", "brand").get(id=product_id)
    context = {
        "title": "SaleMagaz - какой-то товар",
        "product": product,
    }
    return render(request, "goods/product.html", context)
