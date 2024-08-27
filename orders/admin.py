from django.contrib import admin

from orders.models import Order, OrderItem

# admin.site.register(Order)
# admin.site.register(OrderItem)


class OrderItemTabularAdmin(admin.TabularInline):
    model = OrderItem
    fields = ("name", "price", "quantity")
    search_fields = ("product", "name")
    extra = 0


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "name", "price", "quantity")
    search_fields = ("order", "product", "name")


class OrderTabularAdmin(admin.TabularInline):
    model = Order
    fields = ("address", "status", "payment", "note", "created_timestamp")
    search_fields = ("id", "address", "note", "created_timestamp")
    readonly_fields = ("created_timestamp",)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # fields = (
    #     "id",
    #     "user",
    #     "address",
    #     "status",
    #     "payment",
    #     "created_timestamp",
    # )
    # list_display_links = (
    #     "id",
    #     "user",
    #     "address",
    #     "status",
    #     "payment",
    #     "created_timestamp",
    # )
    list_display = (
        "id",
        "user",
        "address",
        "status",
        "payment",
        "created_timestamp",
    )

    search_fields = ("id",)
    readonly_fields = ("created_timestamp",)
    list_filter = (
        "address",
        "status",
        "payment",
    )
    inlines = (OrderItemTabularAdmin,)
