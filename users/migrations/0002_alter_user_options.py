# Generated by Django 4.2.11 on 2024-07-23 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "verbose_name": "Пользователя",
                "verbose_name_plural": "Пользователи",
            },
        ),
    ]
