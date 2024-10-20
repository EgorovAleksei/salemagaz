from django.urls import include, path

from orders import views
from orders.views import OrderDetailView

app_name = "orders"


urlpatterns = [
    path("create-order/", views.CreateOrderView.as_view(), name="create-order"),
    # path("create-order/", views.create_order, name="create-order"),
    path("", views.OrderListView.as_view(), name="orders"),
    # path("", views.orders, name="orders"),
    path("view_order/", views.view_order, name="view_order"),
    path("order/<int:pk>/", OrderDetailView.as_view(), name="order"),
]
