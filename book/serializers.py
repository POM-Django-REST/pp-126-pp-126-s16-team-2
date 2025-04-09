from rest_framework import serializers
from .models import Book  # Імпорт моделі Book з додатку book
from author.models import Author  # Імпорт моделі Author з додатку author

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


