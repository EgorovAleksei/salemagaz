from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.


class Category(MPTTModel):
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
        db_index=True,
        db_column="parent",
        verbose_name="Родительская категория",
    )
    name = models.CharField(verbose_name="Название категории")
    seo = models.CharField(null=True, blank=True)
    url = models.CharField(null=True, blank=True)
    shard = models.CharField(null=True, blank=True)
    query = models.CharField(null=True, blank=True)
    childs = models.BooleanField(default=True)
    published = models.BooleanField(default=True)
    sub_category = models.JSONField(
        blank=True, null=True, default=None, verbose_name="подкатегория"
    )
    filter_category = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "categories"
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name} | {self.id}"


# class CategoryTTT(MPTTModel):
#
#     wb_id = models.IntegerField()
#     parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
#                             db_index=True, db_column='parent', verbose_name='Родительская категория')
#     name = models.CharField(verbose_name='Название категории')
#     seo = models.CharField(null=True, blank=True)
#     url = models.CharField(null=True, blank=True)
#     shard = models.CharField(null=True, blank=True)
#     query = models.CharField(null=True, blank=True)
#     childs = models.BooleanField(default=True)
#     published = models.BooleanField(default=True)
#     sub_category = models.JSONField(blank=True, null=True, default=None, verbose_name='подкатегория')
#     filter_category = models.BooleanField(default=True)
#     created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
#     updated = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         db_table = 'categories_ttt'
#         verbose_name = 'Категорию'
#         verbose_name_plural = 'КатегорииTTT'
#
#     def __str__(self):
#         return f'{self.name} | {self.id}'


class Brand(models.Model):
    wb_id = models.IntegerField()
    name = models.CharField(verbose_name="Название категории")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "brand"
        verbose_name = "Брэнд"
        verbose_name_plural = "Брэнды"

    def __str__(self):
        return f"{self.name} | {self.id}"


#
#
class Products(models.Model):
    # wb_id = models.IntegerField()
    name = models.CharField(verbose_name="Название категории")
    price = models.IntegerField(default=0, verbose_name="цена")
    quantity = models.IntegerField(default=0, verbose_name="количество")
    brand = models.ForeignKey(
        to=Brand,
        db_column="brand",
        on_delete=models.SET_NULL,
        verbose_name="Брэнд",
        null=True,
        blank=True,
    )
    category = TreeForeignKey(
        to=Category,
        db_column="category",
        on_delete=models.CASCADE,
        verbose_name="категория",
        null=True,
    )
    root = models.IntegerField(default=None, verbose_name="Рейтинг")
    subjectId = models.IntegerField(default=None, verbose_name="Под категория")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")
    pics = models.JSONField(verbose_name="Картинки")
    price_history = models.JSONField(verbose_name="история цены")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(default=0, verbose_name="скидка")

    class Meta:
        db_table = "product"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["-updated"]

    def display_id(self):
        return f"Артикул {self.id}"

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100)
        return self.price

    def get_absolute_url(self):
        # print(f"{settings.DOMAIN_NAME}/products/category/{self.category.id}/")

        # return f"{settings.DOMAIN_NAME}/products/category/{self.category.id}/"
        return reverse("goods:product", kwargs={"product_id": self.id})

    def __str__(self):
        return f"{self.name} | {self.id}"
