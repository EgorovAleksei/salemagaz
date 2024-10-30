from django.urls import include, path, reverse

from orders import views


app_name = "orders"


urlpatterns = [
    path("create_order/", views.CreateOrderView.as_view(), name="create_order"),
    # path("create-order/", views.create_order, name="create-order"),
    path("", views.OrderListView.as_view(), name="orders"),
    # path("", views.orders, name="orders"),
    path("view_order/", views.view_order, name="view_order"),
    path("order/<int:pk>/", views.OrderDetailView.as_view(), name="order"),
]

# f"{settings.DOMAIN_NAME}/{reverse('orders:create_order')}"
