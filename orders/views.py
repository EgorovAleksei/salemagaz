from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Prefetch
from django.shortcuts import redirect, render
from django.db import transaction
from django.views.generic import DetailView

from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem, Cart


def view_order(request):
    return render(request, "orders/create_order.html")


@login_required
def create_order(request):
    if request.method == "POST":
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                # пытаемся создать заказ, если хватает товара
                with transaction.atomic():
                    user = request.user

                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data["phone_number"],
                            address=form.cleaned_data["address"],
                            note=form.cleaned_data["note"],
                            payment=form.cleaned_data["payment"],
                            orders_sum=cart_items.total_price(),
                        )

                        for cart_item in cart_items:
                            product = cart_item.product
                            name = cart_item.product.name
                            price = cart_item.product.sell_price()
                            quantity = cart_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(
                                    f"Недостаточно товара {name} на складе. В наличии {product.quantity} заказали {quantity}"
                                )

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )

                            product.quantity -= quantity
                            product.save()

                        # Очищаем корзину пользователя после создания заказа.
                        cart_items.delete()

                        messages.success(request, "Заказ оформлен!")
                        return redirect("user:profile")
            except ValidationError as e:
                messages.error(request, str(e))
                return redirect("cart:order")

    else:
        initial = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        }

        form = CreateOrderForm(data=initial)

    context = {
        "title": "Home Оформление заказа",
        "form": form,
    }
    return render(request, "orders/create_order.html", context=context)


@login_required()
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-id")

    # for order in orders:
    #     # print(order.orderitem_set.all())
    #     for x in order.orderitem_set.all():
    #         print(x.price, x.quantity)

    context = {"orders": orders}
    return render(request, "orders/orders.html", context=context)


class OrderDetailView(DetailView):
    template_name = "orders/order.html"
    context_object_name = "order"
    # model = Order

    def get_queryset(self):
        orders = (
            Order.objects.filter(pk=self.kwargs["pk"])
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
