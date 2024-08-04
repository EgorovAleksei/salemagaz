from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from goods.models import Brand, Category, Products


# @admin.register(CategoryTTT)
# class CategoriesAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name',)
#     #prepopulated_fields = {'slug': ('name',)} # поле которое заполняется автоматически

@admin.register(Category)
class CategoriesAdmin(MPTTModelAdmin):
    list_display = ('id', 'name',)
    #prepopulated_fields = {'slug': ('name',)} # поле которое заполняется автоматически

# @admin.register(CategoryTTT)
# class CategoriesAdmin(MPTTModelAdmin):
#     list_display = ('id', 'name',)
#     #prepopulated_fields = {'slug': ('name',)} # поле которое заполняется автоматически
#


#
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quantity', 'brand', 'category', 'subjectId')
#
#

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')