from rest_framework import serializers
from book.models import Book  # Імпорт із додатку `book`
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

