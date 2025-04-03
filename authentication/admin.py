from django.contrib import admin
from django.contrib.auth.models import Group
from authentication.models import CustomUser  # Імпортуємо CustomUser
from users.models import User  # Імпортуємо User із нового додатка Users

# Відміняємо стандартну реєстрацію групи
admin.site.unregister(Group)

# Кастомна реєстрація групи
@admin.register(Group)
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Відображення назви групи
    search_fields = ('name',)  # Пошук за назвою групи
    ordering = ('name',)  # Сортування груп за назвою

# Реєстрація CustomUser для адміністрації
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'is_superuser')  # Поля для відображення
    search_fields = ('email', 'first_name', 'last_name')  # Пошук
    ordering = ('email',)  # Сортування за email

# Реєстрація User для обліку взаємодії користувачів з книгами
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('viewed_books', 'borrowed_books', 'returned_books')  # Поля для відображення
    search_fields = ('username', 'email')  # Пошук за username та email
    ordering = ('id',)  # Сортування за ID


