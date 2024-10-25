from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Product, Review
from shopOrders.models import Order, OrderItem


caption = "Magic Tricks Shop"


# Create your views here.
def index(request):
    return render(request, 'shopGoods/index.html',
                  {'caption': caption})


def catalog(request):
    products = Product.objects.all()
    user_ordered_products = []

    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            # Пользователь является администратором, предоставляем доступ к каталогу
            user_ordered_products = []
        else:
            # Обычный пользователь
            user_ordered_products = Order.objects.filter(user=request.user).values_list('product__id', flat=True)

    context = {
        'caption': caption,
        'products': products,
        'user_ordered_products': user_ordered_products
    }
    return render(request, 'shopGoods/catalog.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    user_ordered_products = []
    if request.user.is_authenticated:
        user_ordered_products = Order.objects.filter(user=request.user).values_list('product__id', flat=True)
    context = {
        'product': product,
        'reviews': reviews,
        'user_ordered_products': user_ordered_products
    }
    return render(request, 'shopGoods/product_detail.html', context)


@login_required
def review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        text = request.POST.get('text')

        # Проверяем, может ли пользователь оставить отзыв на товар
        if user_can_review(request.user, product):
            Review.objects.create(
                user=request.user,
                product=product,
                text=text,
                rating=int(rating)
            )
            return redirect(reverse('product_detail', args=[product.id]))

    context = {
        'product': product
    }
    return render(request, 'shopGoods/review.html', context)


def user_can_review(user, product):
    # Проверяем, делал ли пользователь заказ на этот товар
    return OrderItem.objects.filter(order__user=user, product=product).exists()


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = request.session.get('cart', {})

        if product_id in cart:
            cart[product_id] += 1
        else:
            cart[product_id] = 1

        request.session['cart'] = cart
        messages.success(request, 'Товар добавлен в корзину!')

    return redirect('shopUsers:cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    # Преобразуем product_id в строку, поскольку ключи в сессии обычно строковые
    str_product_id = str(product_id)

    if str_product_id in cart:
        del cart[str_product_id]
        request.session['cart'] = cart
        messages.success(request, 'Товар удален из корзины!')
    else:
        messages.error(request, 'Товар не найден в корзине.')

    return redirect('shopUsers:cart')
