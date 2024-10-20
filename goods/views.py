import random

from django.core.paginator import Paginator
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import DetailView, ListView
from django.http import Http404

from goods.models import Category, Products
from goods.utils import q_search


class CatalogView(ListView):
    # Вместо model = Products используем get_queryset
    model = Products
    # queryset если надо вместо all что вывести другое.
    # queryset = Products.objects.filter(category=category_id).select_related(
    #     "category", "brand"
    # )
    template_name = "goods/catalog.html"
    context_object_name = "goods"
    paginate_by = 15
    allow_empty = False
    extra_context = {"title": "SaleMagaz - Товары", "category_id": 0}

    def get_queryset(self):

        category_id = self.kwargs.get("category_id", 0)
        if category_id == 0:
            category_id = Category.objects.filter(parent__gt=2).values_list(
                "id", flat=True
            )
            x = random.randint(0, len(category_id) - 1)
            category_id = category_id[x : x + 1][0]
            self.extra_context["category_id"] = category_id

        on_sale = self.request.GET.get("on_sale", None)
        order_by = self.request.GET.get("order_by", None)
        query = self.request.GET.get("q", None)
        price_min = self.request.GET.get("price_min", None)
        price_max = self.request.GET.get("price_max", None)

        if category_id:
            # goods = get_object_or_404(Products.objects.filter(category=category_id).
            #                       select_related('category', 'brand'))
            goods = (
                super()
                .get_queryset()
                .filter(category=category_id)
                .select_related("category", "brand")
            )
            if not goods.exists():
                raise Http404
        elif query:
            goods = q_search(query)
        else:
            goods = super().get_queryset()
            # goods = (
            #     Products.objects.all()
            #     .select_related("category", "brand")
            #     .order_by("-updated")
            # )

        if on_sale:
            goods = goods.filter(discount__gt=0)

        if order_by:
            goods = goods.order_by(order_by)

        if price_max:
            goods = goods.filter(price__lte=price_max)
        if price_min:
            goods = goods.filter(price__gte=price_min)

        return goods


# def catalog(request, category_id=0):
#     page = request.GET.get("page", 1)
#     on_sale = request.GET.get("on_sale", None)
#     order_by = request.GET.get("order_by", None)
#     query = request.GET.get("q", None)
#
#     if category_id:
#         # goods = get_object_or_404(Products.objects.filter(category=category_id).
#         #                       select_related('category', 'brand'))
#         goods = Products.objects.filter(category=category_id).select_related(
#             "category", "brand"
#         )
#     elif query:
#         goods = q_search(query)
#     else:
#         goods = (
#             Products.objects.all()
#             .select_related("category", "brand")
#             .order_by("-updated")
#         )
#     if on_sale:
#         goods = goods.filter(discount__gt=0)
#
#     if order_by:
#         goods = goods.order_by(order_by)
#
#     # goods = get_list_or_404(goods)  не работает почему-то
#     paginator = Paginator(goods, 15)
#     current_page = paginator.page(page)
#
#     context = {
#         "title": "SaleMagaz - Товары",
#         "goods": current_page,
#         "category_id": category_id,
#     }
#
#     return render(request, "goods/catalog.html", context)


class ProductView(DetailView):
    # Если надо выбрать всё, просто указываем model = Products
    # model = Products
    template_name = "goods/product.html"
    context_object_name = "product"
    pk_url_kwarg = "product_id"

    def get_object(self, queryset=None):
        product = Products.objects.select_related("category", "brand").get(
            id=self.kwargs.get(self.pk_url_kwarg)
        )
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name + " - " + str(self.object.id)
        return context


# def product(request, product_id):
#     product = Products.objects.select_related("category", "brand").get(id=product_id)
#     context = {
#         "title": "SaleMagaz - какой-то товар",
#         "product": product,
#     }
#     return render(request, "goods/product.html", context)
