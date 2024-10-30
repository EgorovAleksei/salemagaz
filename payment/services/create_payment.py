from django.http import HttpResponseRedirect
from yookassa import Configuration, Payment
from salemagaz.settings import YOOKASSA_SHOPID, YOOKASSA_SECRET_KEY

Configuration.account_id = YOOKASSA_SHOPID
Configuration.secret_key = YOOKASSA_SECRET_KEY


def create_payment_yookassa(data):
    payment = Payment.create(
        {
            "amount": {"value": data["amount"], "currency": "RUB"},
            "confirmation": {
                "type": "redirect",
                "return_url": "http://127.0.0.1:8000/user/user-cart/",
            },
            "metadata": {
                "user_id": data["user_id"],
                "amount": float(data["amount"]),
            },
            "description": f"Пополнение на {data["amount"]}",
            "capture": True,
        }
    )
    return payment
