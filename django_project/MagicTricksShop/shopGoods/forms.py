from django import forms  # import ModelForm, TextInput
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Текст отзыва'}),
            'rating': forms.RadioSelect(attrs={'class': 'form-control'}),
        }
