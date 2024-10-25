from django.shortcuts import render, redirect
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm
from shopGoods.models import Product
from shopUsers.models import User


# Create your views here.
# def order(request):
#     if request.method == 'POST':
#         order_form = OrderForm(request.POST)
#         if order_form.is_valid():
#             order = order_form.save()
#             products = order_form.cleaned_data['products']
#             for product in products:
#                 OrderItem.objects.create(order=order, product=product,
#                                          quantity=1)
#             return redirect('shopOrders:order_confirmation')
#     else:
#         order_form = OrderForm()
#
#     return render(request, 'shopOrders/order.html', {'order_form': order_form})


# @login_required
# def order(request):
#     if request.method == 'POST':
#         order_form = OrderForm(request.POST)
#         if order_form.is_valid():
#             order = order_form.save(commit=False)
#             order.user = request.user
#             order.save()
#             cart_items = request.session.get('cart', {})
#             for product_id, quantity in cart_items.items():
#                 product = Product.objects.get(id=product_id)
#                 OrderItem.objects.create(order=order, product=product, quantity=quantity)
#             request.session['cart'] = {}  # Clear the cart after order is placed
#             return redirect('shopOrders:order_confirmation')
#     else:
#         order_form = OrderForm()
#     context = {
#         'order_form': order_form,
#         'user': request.user
#     }
#     return render(request, 'shopOrders/order.html', context)

# def order(request):
#     # Проверка, авторизован ли пользователь
#     if not request.user.is_authenticated:
#         return redirect('shopUsers:login')  # Если пользователь не авторизован, перенаправляем на страницу логина
#
#     if request.method == 'POST':
#         order_form = OrderForm(request.POST)
#         if order_form.is_valid():
#             order = order_form.save(commit=False)
#             order.user = request.user  # Привязываем заказ к текущему пользователю
#             order.save()
#
#             # Получаем товары из корзины
#             cart_items = request.session.get('cart', {})
#             for product_id, quantity in cart_items.items():
#                 product = Product.objects.get(id=product_id)
#                 OrderItem.objects.create(order=order, product=product, quantity=quantity)
#
#             # Очищаем корзину после оформления заказа
#             request.session['cart'] = {}
#
#             # Перенаправляем на страницу подтверждения заказа
#             return redirect('shopOrders:order_confirmation')
#
#     else:
#         order_form = OrderForm()
#
#     context = {'order_form': order_form}
#     return render(request, 'shopOrders/order.html', context)


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
    return render(request, 'shopOrders/history.html')
