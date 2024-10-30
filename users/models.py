from __future__ import annotations
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models, transaction
from django.core.validators import MinValueValidator
from decimal import Decimal

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.timezone import now


def is_amount_positive(method):
    def wrapper(cls, *args, **kwargs):
        amount = kwargs["amount"]
        if amount < 0:
            raise ValueError("Should be positive value")
        return method(cls, *args, **kwargs)

    return wrapper


class User(AbstractUser):
    image = models.ImageField(upload_to="users_images", null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    balance = models.DecimalField(
        decimal_places=2,
        max_digits=settings.MAX_BALANCE_DIGITS,
        validators=[MinValueValidator(0, message="Insufficient Funds")],
        default=0,
    )

    class Meta:
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"

    @classmethod
    @is_amount_positive
    def deposit(cls, *, pk: int, amount: Decimal) -> User:

        with transaction.atomic():
            user = get_object_or_404(
                cls.objects.select_for_update(),
                pk=pk,
            )
            user.balance += amount
            user.save()
        return user

    @classmethod
    @is_amount_positive
    def withdraw(cls, *, pk: int, amount: Decimal) -> User:
        with transaction.atomic():
            user = get_object_or_404(
                cls.objects.select_for_update(),
                pk=pk,
            )
            user.balance -= amount
            user.save()
        return user

    def __str__(self):
        return self.username
