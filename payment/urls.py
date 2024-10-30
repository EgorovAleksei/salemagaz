from django.urls import path

from . import views


app_name = "payment"


urlpatterns = [
    path("create_payment/", views.CreatePaymentView.as_view(), name="create_payment"),
    path(
        "create_payment/<str:amount>",
        views.CreatePaymentView.as_view(),
        name="create_payment",
    ),
    # path(
    #     "payment_acceptance/",
    #     views.CreatePaymentAcceptanceView.as_view(),
    #     name="payment_acceptance",
    # ),
    path(
        "payment_acceptance/", views.crate_payment_acceptance, name="payment_acceptance"
    ),
]
