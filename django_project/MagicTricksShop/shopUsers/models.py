from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class User(models.Model):
    name = models.CharField('Имя', max_length=50, unique=True)
    email = models.EmailField('Email', max_length=100)
    phone = PhoneNumberField('Телефон', max_length=20)
    address = models.CharField('Адрес', max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
