from django.shortcuts import render


# Create your views here.
def register(request):
    return render(request, 'shopUsers/register.html')


def login(request):
    return render(request, 'shopUsers/login.html')


def cabinet(request):
    return render(request, 'shopUsers/cabinet.html')


# страница не нужна?
def logout(request):
    return render(request, 'shopUsers/logout.html')


def cart(request):
    return render(request, 'shopUsers/cart.html')
