# shopOrders/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum, F
from .models import Order, OrderItem, Report


@receiver(post_save, sender=Order)
def create_report_on_order_completion(sender, instance, **kwargs):
    # Проверяем, что заказ завершен
    if instance.status == 'completed':
        # Подсчет данных по продажам
        sales_data = OrderItem.objects.filter(order=instance).values(
            'product__name'
        ).annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(F('quantity') * F('product__price'))
        )

        # Подсчет общей прибыли для завершенного заказа
        total_profit = sum(item['total_revenue'] for item in sales_data)

        # Формируем строку данных по продажам
        sales_data_str = "; ".join(
            f"{item['product__name']}: {item['total_quantity']} шт., Выручка: {item['total_revenue']} руб."
            for item in sales_data
        )

        # Создание отчета
        Report.objects.create(
            order=instance,
            sales_data=sales_data_str,
            profit=total_profit,
            expenses=0  # Значение расходов можно установить позже
        )
