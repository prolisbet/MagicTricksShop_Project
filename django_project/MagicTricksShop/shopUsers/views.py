from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import UserForm
from shopGoods.models import Product


# Create your views here.
def register(request):
    error = ''
    if request.method == 'POST':
        form = UserForm(request.POST)  # Сюда сохранится информация от пользователя.
        if form.is_valid():
            form.save()
            return redirect('shopUsers:login')
        else:
            error = "Данные были заполнены некорректно"
    form = UserForm()
    return render(request, 'shopUsers/register.html', {'form': form, 'error': error})


def login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        # Проверка наличия пользователя в базе данных
        try:
            user = User.objects.get(name=name, phone=phone)
            # Успешный вход: сохраняем id пользователя в сессии
            request.session['user_id'] = user.id
            return redirect('shopUsers:cabinet')
        except User.DoesNotExist:
            # Если пользователь не найден, добавляем сообщение об ошибке
            messages.error(request, "Пользователь с такими данными не найден.")

    return render(request, 'shopUsers/login.html')


def cabinet(request):
    return render(request, 'shopUsers/cabinet.html')


# @login_required
def edit_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Вам необходимо войти в систему для редактирования профиля.')
        return redirect('shopUsers:login')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Пользователь не найден.')
        return redirect('shopUsers:login')

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
            return redirect('shopUsers:cabinet')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки ниже.')
    else:
        form = UserForm(instance=user)

    return render(request, 'shopUsers/edit_profile.html', {'form': form})

    # if request.method == 'POST':
    #     form = UserForm(request.POST, instance=request.user)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Ваш профиль был успешно обновлен!')
    #         return redirect('shopUsers:cabinet')
    #     else:
    #         messages.error(request, 'Пожалуйста, исправьте ошибки ниже.')
    # else:
    #     form = UserForm(instance=request.user)
    #
    # return render(request, 'shopUsers/edit_profile.html', {'form': form})


def logout(request):
    auth_logout(request)  # Завершаем сеанс пользователя
    return render(request, 'shopUsers/logout_success.html')


def cart(request):
    cart_items = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart_items.keys())

    # Создаем список продуктов с количеством
    products_with_quantity = []
    for product in products:
        quantity = cart_items.get(str(product.id), 0)
        products_with_quantity.append({
            'product': product,
            'quantity': quantity,
        })

    total_price = sum(item['quantity'] * item['product'].price for item in products_with_quantity)

    context = {
        'products_with_quantity': products_with_quantity,
        'total_price': total_price,
        'user': request.user
    }

    return render(request, 'shopUsers/cart.html', context)
