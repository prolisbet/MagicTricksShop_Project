from django.shortcuts import render


# Create your views here.
def order(request):
    return render(request, 'shopOrders/order.html')


def history(request):
    return render(request, 'shopOrders/history.html')


# функция не нужна?
def reorder(request):
    return render(request, 'shopOrders/reorder.html')
