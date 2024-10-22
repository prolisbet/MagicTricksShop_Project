from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('', views.cabinet, name='cabinet'),
    path('logout', views.logout, name='logout'),  # не нужна?
    path('cart', views.cart, name='cart'),
]
