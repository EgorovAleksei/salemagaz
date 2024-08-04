from django.urls import include, path

from carts import views

app_name = "carts"

urlpatterns = [
    # путь чистого джанго
    # path("cart-add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart-add/", views.cart_add, name="cart_add"),
    path("cart-change/", views.cart_change, name="cart_change"),
    path("cart-remove/", views.cart_remove, name="cart_remove"),
]
