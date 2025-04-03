from django.contrib import admin
from .models import User

# Перевіряємо, чи модель вже зареєстрована
if not admin.site.is_registered(User):
    @admin.register(User)
    class UserAdmin(admin.ModelAdmin):
        list_display = ('username', 'email', 'first_name', 'last_name', 'viewed_books', 'borrowed_books', 'returned_books')  # Поля, які відображаються у списку
        search_fields = ('username', 'email')  # Поля для пошуку
        list_filter = ('is_staff', 'is_superuser', 'is_active')  # Фільтри
        ordering = ('-date_joined',)  # Сортування за датою реєстрації
