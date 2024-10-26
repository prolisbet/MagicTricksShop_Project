from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Avg, Count
from .models import Product, Review
from shopOrders.models import Order, OrderItem
from shopUsers.models import User
from .forms import ReviewForm


caption = "Magic Tricks Shop"


# Create your views here.
def index(request):
    return render(request, 'shopGoods/index.html',
                  {'caption': caption})


def catalog(request):
    products = Product.objects.all().annotate(
        review_count=Count('review'),  # Количество отзывов на каждый продукт
        average_rating=Avg('review__rating')  # Средний рейтинг
    )

    user_ordered_products = set()

    user_id = request.session.get('user_id')

    if not request.user.is_staff or not request.user.is_superuser:
        orders = Order.objects.filter(user_id=user_id)
        for order in orders:
            order_items = OrderItem.objects.filter(order_id=order.id)
            for item in order_items:
                user_ordered_products.add(str(item.product_id))

    context = {
        'caption': caption,
        'products': products,
        'user_ordered_products': user_ordered_products
    }
    return render(request, 'shopGoods/catalog.html', context)


def product_detail(request, product_id):
    user_id = request.session.get('user_id')
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product=product)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] if reviews.exists() else 0
    added_to_cart = False
    if request.method == 'POST':
        added_to_cart = True
    user_ordered_products = OrderItem.objects.filter(order__user_id=user_id).values_list('product_id', flat=True)
    # Вычисляем количество отзывов
    last_digit = str(reviews.count() % 10)
    last_two_digits = str(reviews.count() % 100)
    if len(last_two_digits) == 1:
        last_two_digits = '0' + last_two_digits
    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
        'user_ordered_products': user_ordered_products,
        'added_to_cart': added_to_cart,
        'last_digit': last_digit,
        'last_two_digits': last_two_digits
    }
    return render(request, 'shopGoods/product_detail.html', context)


def review(request, product_id):
    user_id = request.session.get('user_id')
    print(f"Current user_id in session: {user_id}")
    if not user_id:
        return redirect('shopUsers:login')

    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid() and user_can_review(user_id, product):
            # Use user_id directly to prevent session conflict
            review = Review(
                product=product,
                user_id=user_id,  # Ensure correct user is assigned
                rating=form.cleaned_data['rating'],
                text=form.cleaned_data['text']
            )
            review.save()
            return redirect(reverse('shopGoods:product_detail', args=[product.id]))
    else:
        form = ReviewForm()

    context = {'product': product, 'form': form}
    return render(request, 'shopGoods/review.html', context)


def user_can_review(user_id, product):
    return OrderItem.objects.filter(order__user_id=user_id, product=product).exists()


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
