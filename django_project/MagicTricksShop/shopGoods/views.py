from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Product, Review


# Create your views here.
def index(request):
    return render(request, 'shopGoods/index.html')


def catalog(request):
    return render(request, 'shopGoods/catalog.html')


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

    return HttpResponse("Тут должна быть форма для добавления отзыва.")

    # return render(request, 'shopGoods/review.html')


def user_can_review(user, product):
    # Простая проверка, может ли пользователь оставить отзыв
    # Например, проверка, делал ли пользователь заказ на этот товар
    # Для примера, всегда возвращаем True
    return True
