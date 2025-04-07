from django import forms
from .models import Book, LibraryMember

class LibraryMemberForm(forms.ModelForm):
    class Meta:
        model = LibraryMember
        fields = ['user', 'borrowed_books']  # Додайте поля, які потрібні для редагування

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'  # Відображення всіх полів моделі Book
