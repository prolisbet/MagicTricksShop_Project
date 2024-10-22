from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField('Имя', max_length=200)
    email = models.CharField('Email', max_length=200)
    phone = models.CharField('Телефон', max_length=200)
    adress = models.CharField('Адрес', max_length=200)
    # password = models.CharField('Пароль', max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
