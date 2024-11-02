from decimal import Decimal

from payment.models import BalanceChange
from users.models import User


def payment_acceptance(response):
    if response["event"] != "payment.succeeded":
        return False
    print("Выполнение payment_acceptance")
    user_id = User.objects.get(pk=response["object"]["metadata"]["user_id"])
    amount = Decimal(response["object"]["amount"]["value"])
    BalanceChange.objects.create(user_id=user_id, amount=amount, operation_type="DT")
    User.deposit(pk=response["object"]["metadata"]["user_id"], amount=amount)
    return True
