from django.contrib import admin, messages
from django.db.models import Sum, F
from .models import Order, OrderItem, Report


# Register your models here.
def generate_sales_report(modeladmin, request, queryset):
    # Общее количество завершенных заказов
    total_sales = Order.objects.filter(status='completed').count()

    # Общая прибыль
    total_profit = Order.objects.filter(status='completed').aggregate(
        total=Sum(F('orderitem__quantity') * F('orderitem__product__price'))
    )['total'] or 0

    # Информация о продажах для выбранных заказов
    for order in queryset:
        if order.status == 'completed':
            sales_data = OrderItem.objects.filter(order=order).values(
                'product__name'
            ).annotate(
                total_quantity=Sum('quantity'),
                total_revenue=Sum(F('quantity') * F('product__price'))
            )

            order_profit = sum(item['total_revenue'] for item in sales_data)
            sales_data_str = "; ".join(
                f"{item['product__name']}: {item['total_quantity']} шт., Выручка: {item['total_revenue']} руб."
                for item in sales_data
            )

            # Создание отчета
            Report.objects.create(
                order=order,
                sales_data=sales_data_str,
                profit=order_profit,
                expenses=0  # Значение расходов можно установить позже
            )

    # Вывод сообщения администратору с общей информацией
    summary_message = (
        f"Общее количество завершенных заказов: {total_sales}\n"
        f"Общая прибыль: {total_profit} руб."
    )
    messages.info(request, summary_message)


generate_sales_report.short_description = "Сгенерировать отчет по продажам"


class OrderAdmin(admin.ModelAdmin):
    actions = [generate_sales_report]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Report)
