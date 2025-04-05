from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


# Тимчасова домашня сторінка
def temporary_home(request):
    return render(request, 'home.html')  # Виправлено шлях до шаблону домашньої сторінки


urlpatterns = [
    path("admin/", admin.site.urls),  # Адміністративна панель
    path("authentication/", include("authentication.urls")),  # Підключення маршрутів authentication
    path("orders/", include("order.urls")),  # Підключення маршрутів для замовлень
    path("", temporary_home, name="home"),  # Маршрут для домашньої сторінки
    path("authors/", include("author.urls")),  # Підключення маршрутів для авторів
    path("books/", include("book.urls")),  # Підключення маршрутів для книг
    path("users/", include("users.urls")),  # Підключення маршрутів для користувачів
]





