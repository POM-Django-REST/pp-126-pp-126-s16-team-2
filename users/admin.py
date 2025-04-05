from django.contrib import admin
from .models import User


# Перевіряємо, чи модель вже зареєстрована
if not admin.site.is_registered(User):
    @admin.register(User)
    class UserAdmin(admin.ModelAdmin):
        list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')  # Поля, які відображаються у списку
        search_fields = ('username', 'email', 'first_name', 'last_name')  # Поля для пошуку
        list_filter = ('is_staff', 'is_superuser', 'is_active')  # Фільтри
        ordering = ('-date_joined',)  # Сортування за датою реєстрації
        readonly_fields = ('viewed_books_count', 'borrowed_books_count', 'returned_books_count')  # Поля тільки для читання

        def viewed_books_count(self, obj):
            """Повертає кількість книг, переглянутих користувачем."""
            return obj.viewed_books.count()

        def borrowed_books_count(self, obj):
            """Повертає кількість книг, взятих користувачем."""
            return obj.borrowed_books.count()

        def returned_books_count(self, obj):
            """Повертає кількість книг, повернутих користувачем."""
            # Залежить від вашої логіки обчислення повернутих книг
            return getattr(obj, 'returned_books', 0)
