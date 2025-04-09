from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'email', 
            'role',  # якщо це поле існує
            'is_active'  # статус активності користувача
        ]
        labels = {
            'first_name': 'Ім\'я',
            'last_name': 'Прізвище',
            'email': 'Електронна пошта',
            'role': 'Роль',  # якщо необхідно
            'is_active': 'Активний користувач',  # якщо включено
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть ім\'я'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть прізвище'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@example.com'}),
            'role': forms.Select(attrs={'class': 'form-select'}),  # Якщо поле 'role' — це CharField із вибором
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

