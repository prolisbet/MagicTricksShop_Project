from django.forms import ModelForm
from django import forms
from .models import Order, OrderItem
from shopGoods.models import Product


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_address']
        widgets = {
            'order_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Адрес доставки',
                'id': 'address',
            })
        }
        labels = {
            'order_address': 'Адрес доставки',
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)


class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        labels = {
            'product': 'Товар',
            'quantity': 'Количество',
        }
