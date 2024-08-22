from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to="users_images", null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
