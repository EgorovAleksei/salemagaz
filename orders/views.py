from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db.models import Prefetch
from django.shortcuts import redirect, render
from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, ListView

from common.mixin import CacheMixin
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem, Cart
from orders.utils import create_order
from django.http import Http404, HttpResponsePermanentRedirect, HttpResponseRedirect


def view_order(request):
    return render(request, "orders/create_order.html")


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = "orders/create_order.html"
    form_class = CreateOrderForm
    success_url = reverse_lazy("user:profile")

    def get_initial(self):
        initial = super().get_initial()

        initial["first_name"] = self.request.user.first_name
        initial["last_name"] = self.request.user.last_name
        initial["phone_number"] = self.request.user.phone_number
        return initial

    def form_valid(self, form):
        return create_order(self.request, form)

    # def form_invalid(self, form):
    #     print(form.errors)
    #     messages.error(self.request, "Заполните поля")
    #     print(messages.error(self.request, "Заполните поля"))
    #     return redirect("orders:create-order")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Salemagaz - Оформление заказа"
        return context


class OrderListView(LoginRequiredMixin, CacheMixin, ListView):
    template_name = "orders/orders.html"
    context_object_name = "orders"
    # model = Order

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     orders = cache.get(f"orders_for_user_{self.request.user.id}")
    #     if not orders:
    #         orders = Order.objects.filter(user=self.request.user).order_by("-id")
    #         cache.set(f"orders_for_user_{self.request.user.id}", orders, 60)
    #     context["orders"] = orders
    #     return context

    def get_queryset(self):
        orders = self.set_get_cache(
            Order.objects.filter(user=self.request.user).order_by("-id"),
            f"orders_for_user_{self.request.user.id}",
            10,
        )
        return orders


class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = "orders/order.html"
    context_object_name = "order"
    # model = Order

    def get_queryset(self):
        orders = (
            Order.objects.filter(pk=self.kwargs["pk"], user=self.request.user)
            .prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            )
            .order_by("-id")
        )
        if not orders:
            orders = Order.objects.filter(user=self.request.user).order_by("-id")

            self.kwargs["pk"] = orders[0].id
            orders = (
                Order.objects.filter(pk=self.kwargs["pk"], user=self.request.user)
                .prefetch_related(
                    Prefetch(
                        "orderitem_set",
                        queryset=OrderItem.objects.select_related("product"),
                    )
                )
                .order_by("-id")
            )
        return orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"SaleMagaz - Заказ #{self.object.id}"
        return context


# @login_required()
# def orders(request):
#     orders = Order.objects.filter(user=request.user).order_by("-id")
#     context = {"orders": orders}
#     return render(request, "orders/orders.html", context=context)

# @login_required
# def create_order(request):
#     if request.method == "POST":
#         form = CreateOrderForm(data=request.POST)
#         if form.is_valid():
#             try:
#                 # пытаемся создать заказ, если хватает товара
#                 with transaction.atomic():
#                     user = request.user
#
#                     cart_items = Cart.objects.filter(user=user)
#
#                     if cart_items.exists():
#                         order = Order.objects.create(
#                             user=user,
#                             phone_number=form.cleaned_data["phone_number"],
#                             address=form.cleaned_data["address"],
#                             note=form.cleaned_data["note"],
#                             payment=form.cleaned_data["payment"],
#                             orders_sum=cart_items.total_price(),
#                         )
#
#                         for cart_item in cart_items:
#                             product = cart_item.product
#                             name = cart_item.product.name
#                             price = cart_item.product.sell_price()
#                             quantity = cart_item.quantity
#
#                             if product.quantity < quantity:
#                                 raise ValidationError(
#                                     f"Недостаточно товара {name} на складе. В наличии {product.quantity} заказали {quantity}"
#                                 )
#
#                             OrderItem.objects.create(
#                                 order=order,
#                                 product=product,
#                                 name=name,
#                                 price=price,
#                                 quantity=quantity,
#                             )
#
#                             product.quantity -= quantity
#                             product.save()
#
#                         # Очищаем корзину пользователя после создания заказа.
#                         cart_items.delete()
#
#                         messages.success(request, "Заказ оформлен!")
#                         return redirect("user:profile")
#             except ValidationError as e:
#                 messages.error(request, str(e))
#                 return redirect("cart:order")
#
#     else:
#         initial = {
#             "first_name": request.user.first_name,
#             "last_name": request.user.last_name,
#         }
#
#         form = CreateOrderForm(data=initial)
#
#     context = {
#         "title": "Home Оформление заказа",
#         "form": form,
#     }
#     return render(request, "orders/create_order.html", context=context)
