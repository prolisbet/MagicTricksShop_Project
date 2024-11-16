from django.shortcuts import render, redirect
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm
from shopGoods.models import Product
from shopUsers.models import User


# Create your views here.
def order(request):
    if not request.session.get('user_id'):
        return redirect('shopUsers:login')  # Проверка, что пользователь авторизован

    # Создаем список продуктов с количеством
    products_with_quantity = []

    # Получаем товары из корзины
    cart_items = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart_items.keys())

    # Перебираем продукты и добавляем их в products_with_quantity
    for product in products:
        quantity = cart_items.get(str(product.id), 0)
        products_with_quantity.append({
            'product': product,
            'quantity': quantity,
        })

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user = User.objects.get(id=request.session['user_id'])  # Получаем текущего пользователя

            # Сохраняем заказ
            order.save()

            # Перебираем продукты и создаем объекты OrderItem
            for item in products_with_quantity:
                OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'])

            # Очищаем корзину после оформления заказа
            request.session['cart'] = {}
            return redirect('shopOrders:order_confirmation')

    else:
        order_form = OrderForm()

    # Подсчет итоговой суммы для отображения
    total_price = sum(item['product'].price * item['quantity'] for item in products_with_quantity)

    context = {
        'order_form': order_form,
        'products_with_quantity': products_with_quantity,
        'total_price': total_price,
    }
    return render(request, 'shopOrders/order.html', context)


def order_confirmation(request):
    return render(request, 'shopOrders/order_confirmation.html')


def history(request):
    if not request.session.get('user_id'):
        return redirect('shopUsers:login')

    user = User.objects.get(id=request.session['user_id'])
    orders = Order.objects.filter(user=user).prefetch_related('orderitem_set__product')

    # Добавляем финальную стоимость и список товаров для каждого заказа
    for order in orders:
        order_items = order.orderitem_set.all()
        total_cost = sum(item.quantity * item.product.price for item in order_items)
        for item in order_items:
            item.total_price = item.quantity * item.product.price
        order.total_cost = total_cost
        order.order_items = order_items

    context = {
        'orders': orders
    }
    return render(request, 'shopOrders/history.html', context)
