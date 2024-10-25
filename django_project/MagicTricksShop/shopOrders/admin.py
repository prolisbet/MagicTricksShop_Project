from django.contrib import admin
from django.db.models import Sum, F
from .models import Order, OrderItem, Report


# Register your models here.
def generate_sales_report(modeladmin, request, queryset):
    # Общее количество завершенных заказов
    total_sales = Order.objects.filter(status='completed').count()
    print(f'Общее количество завершенных заказов: {total_sales}')

    # Общая прибыль
    total_profit = Order.objects.filter(status='completed').aggregate(
        total=Sum(F('orderitem__quantity') * F('orderitem__product__price'))
    )['total']
    print(f'Общая прибыль: {total_profit}')

    # Количество и прибыль по каждой позиции
    sales_by_product = OrderItem.objects.filter(order__status='completed').values(
        'product__name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('product__price'))
    )

    for item in sales_by_product:
        print(f"Товар: {item['product__name']}, Количество: {item['total_quantity']}, Выручка: {item['total_revenue']}")


generate_sales_report.short_description = "Сгенерировать отчет по продажам"


class OrderAdmin(admin.ModelAdmin):
    actions = [generate_sales_report]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Report)
