from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Product(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    description = models.TextField('Краткое описание', max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='shopGoods/media/', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    text = models.TextField('Отзыв', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(
        'Рейтинг',
        choices=[(i, str(i)) for i in range(1, 6)]
    )
    review_date = models.DateTimeField('Дата', auto_now_add=True)

    def __str__(self):
        return f'Отзыв от {self.user.name} на {self.product.name}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
