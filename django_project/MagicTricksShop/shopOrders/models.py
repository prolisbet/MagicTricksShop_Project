from django.db import models
from shopUsers.models import User
from shopGoods.models import Product


# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидается'),
        ('processing', 'В обработке'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    products = models.ManyToManyField(
        Product,
        through='OrderItem',
        verbose_name='Товары'
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    order_date = models.DateTimeField('Дата заказа', auto_now_add=True)
    order_address = models.TextField('Адрес доставки', null=True, blank=True)

    def __str__(self):
        return f'Заказ {self.id} от {self.user.name}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Количество', default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} для заказа {self.order.id}'


class Report(models.Model):
    date = models.DateField('Дата', auto_now_add=True)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ'
    )
    sales_data = models.TextField('Данные по продажам')
    profit = models.DecimalField('Прибыль', max_digits=10, decimal_places=2)
    expenses = models.DecimalField('Расходы', max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'Отчет {self.id} за {self.date}'

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'
