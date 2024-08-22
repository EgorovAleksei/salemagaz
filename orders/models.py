from django.db import models
from django.urls import reverse

from carts.models import Cart
from goods.models import Products
from salemagaz import settings
from users.models import User


class OrderitemQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WEY = 2
    DELIVERED = 3
    STATUS = (
        (CREATED, "Создан"),
        (PAID, "Оплачен"),
        (ON_WEY, "В пути"),
        (DELIVERED, "Доставлен"),
    )

    CARD = 0
    SBP = 1
    CASH = 2
    PAYMENT = (
        (CARD, "Картой"),
        (SBP, "СБП"),
        (CASH, "Наличными"),
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_DEFAULT,
        blank=True,
        null=True,
        verbose_name="Пользователь",
        default=None,
    )
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания заказа"
    )

    first_name = models.CharField(max_length=64, verbose_name="Имя")
    last_name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    address = models.CharField(max_length=256)
    note = models.TextField(verbose_name="Примечание")
    status = models.SmallIntegerField(default=CREATED, choices=STATUS)
    payment = models.SmallIntegerField(default=CREATED, choices=PAYMENT)

    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_timestamp"]

    def __str__(self):
        return f"Заказ №{self.id}. Покупатель{self.first_name} {self.last_name}"

    # def update_after_payment(self):
    #     baskets = Cart.objects.filter(user=self.user)
    #     self.status = self.PAID
    #     self.basket_history = {
    #         "purchased_item": [basket.de_json() for basket in baskets],
    #         "total_sum": float(baskets.total_sum()),
    #     }
    #     baskets.delete()
    #     self.save()

    def get_absolute_url(self):
        # f"{settings.DOMAIN_NAME}/products/category/{self.category.id}/"
        # return reverse('orders:order', kwargs={'pk': self.id}) не работает т.к. SITE_ID
        return settings.DOMAIN_NAME + reverse("orders:order", kwargs={"pk": self.id})


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(
        to=Products,
        on_delete=models.SET_DEFAULT,
        null=True,
        verbose_name="Продукт",
        default=None,
    )
    name = models.CharField(max_length=150, verbose_name="Название")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата продажи"
    )

    class Meta:
        db_table = "order_item"
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"
        ordering = ("id",)

    objects = OrderitemQueryset.as_manager()

    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self):
        return f"Товар {self.name} | Заказ № {self.order.pk}"
