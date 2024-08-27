from django.urls import include, path

from orders import views

app_name = "orders"

urlpatterns = [
    path("create-order/", views.create_order, name="create-order"),
    path("view_order/", views.view_order, name="view_order"),
]
