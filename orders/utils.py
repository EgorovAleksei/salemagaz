from orders.models import Order, OrderItem, Cart
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import redirect, render


def create_order(request, form):
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
