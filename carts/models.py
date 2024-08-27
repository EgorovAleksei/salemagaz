from django.db import models

from goods.models import Products
from users.models import User


class CartQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

    def sub_total_price(self):
        return sum(cart.sub_products_price() for cart in self)


class Cart(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Пользователь",
    )
    product = models.ForeignKey(
        to=Products, on_delete=models.CASCADE, verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        db_table = "cart"
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        ordering = ["pk"]

    objects = CartQueryset.as_manager()

    def products_price(self):
        return self.product.sell_price() * self.quantity

    def sub_products_price(self):
        return self.product.price * self.quantity

    def pr_name(self):
        return self.product.name

    def __str__(self):
        if self.user:
            return f"Корзина {self.user.username} | Товар {self.product.name} | Количество {self.quantity}"
        return f"Корзина Анонимная корзина | Товар {self.product.name} | Количество {self.quantity}"
