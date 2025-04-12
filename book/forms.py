from django import forms
from .models import Book, LibraryMember
from author.models import Author

class BookForm(forms.ModelForm):
    new_author = forms.CharField(required=False, label="Новий автор")

    class Meta:
        model = Book
        fields = ['name', 'description', 'count', 'authors']  # Або '__all__' якщо потрібно всі поля

class LibraryMemberForm(forms.ModelForm):
    class Meta:
        model = LibraryMember
        fields = ['user', 'borrowed_books']
