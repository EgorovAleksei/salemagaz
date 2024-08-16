from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from goods.models import Brand, Category, Products


# @admin.register(CategoryTTT)
# class CategoriesAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name',)
#     #prepopulated_fields = {'slug': ('name',)} # поле которое заполняется автоматически


@admin.register(Category)
class CategoriesAdmin(MPTTModelAdmin):
    list_display = (
        "id",
        "name",
    )
    # prepopulated_fields = {'slug': ('name',)} # поле которое заполняется автоматически


# @admin.register(CategoryTTT)
# class CategoriesAdmin(MPTTModelAdmin):
#     list_display = ('id', 'name',)
#     #prepopulated_fields = {'slug': ('name',)} # поле которое заполняется автоматически
#


#
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "quantity",
        "brand",
        "category",
        "subjectId",
    )  # отображаемые поля в админке
    list_per_page = 80
    list_editable = ("quantity",)  # редактируемые поля
    search_fields = ("name", "id")  # по каким полям искать
    list_filter = ("category", "brand", "subjectId")  # справа панель фильтров
    fields = ("name", "category", ("quantity", "brand"), "subjectId")


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
