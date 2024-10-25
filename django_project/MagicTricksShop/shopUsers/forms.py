from .models import User
from django.forms import ModelForm, TextInput, EmailInput
from django.forms.fields import CharField
from phonenumber_field.formfields import PhoneNumberField


class UserForm(ModelForm):

    phone = PhoneNumberField(widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Телефон',
        'id': 'phone',
    }))

    address = CharField(required=False, widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Адрес',
        'id': 'address',
    }))

    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'address']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя', 'id': 'name'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'id': 'email'}),
        }
