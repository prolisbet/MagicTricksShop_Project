from django.urls import path
from . import views

urlpatterns = [
    path('', views.order, name='order'),
    path('history', views.history, name='history'),
    path('reorder', views.reorder, name='reorder'),  # не нужна?
]
