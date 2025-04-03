from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'viewed_books', 'borrowed_books', 'returned_books']
        labels = {
            'first_name': 'Ім\'я',
            'last_name': 'Прізвище',
            'email': 'Ел. пошта',
            'viewed_books': 'Переглянуті книги',
            'borrowed_books': 'Взяті книги',
            'returned_books': 'Повернуті книги',
        }
