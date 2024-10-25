from django.urls import path
from . import views

app_name = 'shopUsers'

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('', views.cabinet, name='cabinet'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('logout', views.logout, name='logout'),
    path('cart', views.cart, name='cart'),
]
