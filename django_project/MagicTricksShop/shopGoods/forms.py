from django.forms import ModelForm, TextInput
from .models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': TextInput(attrs={'class': 'form-control', 'placeholder': 'Текст отзыва'}),
            'rating': TextInput(attrs={'class': 'form-control', 'placeholder': 'Рейтинг отзыва'}),
        }
