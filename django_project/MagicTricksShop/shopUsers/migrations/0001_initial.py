# Generated by Django 5.1.2 on 2024-10-24 16:21

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Имя')),
                ('email', models.EmailField(max_length=100, verbose_name='Email')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=20, region=None, verbose_name='Телефон')),
                ('address', models.CharField(blank=True, null=True, max_length=200, verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
