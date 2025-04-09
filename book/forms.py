from django import forms
from .models import Book, LibraryMember
<<<<<<< HEAD
from author.models import Author

class BookForm(forms.ModelForm):
    new_author = forms.CharField(required=False, label="Новий автор")

    class Meta:
        model = Book
        fields = ['name', 'description', 'count', 'authors']
=======
>>>>>>> Daniil

class LibraryMemberForm(forms.ModelForm):
    class Meta:
        model = LibraryMember
        fields = ['user', 'borrowed_books']  # Додайте поля, які потрібні для редагування

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'  # Відображення всіх полів моделі Book
