from django.contrib import admin

from carts.models import Cart

# admin.site.register(Cart)


class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = ("quantity", "created")
    list_display = ("__str__",)
    # search_fields = ("product", "quantity", "created")
    readonly_fields = ("created",)
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "product_display", "quantity", "created")
    list_filter = ("user",)

    # def user_display(self, obj):
    #     if obj.user:
    #         return str(obj.user)
    #     return "Анонимный пользователь"

    @admin.display(description="Продукт")
    def product_display(self, obj):
        return str(obj.product.name)
