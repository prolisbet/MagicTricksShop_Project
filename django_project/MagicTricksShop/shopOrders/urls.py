from django.urls import path
from . import views

app_name = 'shopOrders'

urlpatterns = [
    path('', views.order, name='order'),
    path('history', views.history, name='history'),
    path('order_confirmation', views.order_confirmation, name='order_confirmation'),
]
