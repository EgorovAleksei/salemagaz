from django.core.validators import MinValueValidator
from rest_framework import serializers

from salemagaz import settings


class CreatePaymentSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    amount = serializers.DecimalField(
        decimal_places=2,
        max_digits=settings.MAX_BALANCE_DIGITS,
        validators=[MinValueValidator(0, message="Insufficient Funds")],
    )
    return_url = serializers.URLField()
