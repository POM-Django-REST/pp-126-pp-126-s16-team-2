from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
<<<<<<< HEAD

=======
from rest_framework.routers import DefaultRouter
from users import views as users_views
from order import views as order_views
>>>>>>> Daniil

# Тимчасова домашня сторінка
def temporary_home(request):
    return render(request, 'home.html')  # Виправлено шлях до шаблону домашньої сторінки

<<<<<<< HEAD
=======
router = DefaultRouter()
router.register(r'api/v1/user', users_views.UserViewSet, basename='user')
router.register(r'api/v1/order', order_views.OrderViewSet, basename='order')
>>>>>>> Daniil

urlpatterns = [
    path("admin/", admin.site.urls),  # Адміністративна панель
    path("authentication/", include("authentication.urls")),  # Підключення маршрутів authentication
    path("orders/", include("order.urls")),  # Підключення маршрутів для замовлень
    path("", temporary_home, name="home"),  # Маршрут для домашньої сторінки
    path("authors/", include("author.urls")),  # Підключення маршрутів для авторів
    path("books/", include("book.urls")),  # Підключення маршрутів для книг
    path("users/", include("users.urls")),  # Підключення маршрутів для користувачів
<<<<<<< HEAD
=======
    path('api/v1/user/<int:user_id>/order/', order_views.UserOrderViewSet.as_view({'get': 'list'})),
    path('', include(router.urls)),
    path('api/v1/user/<int:user_id>/order/<int:pk>/', order_views.OrderViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
>>>>>>> Daniil
]





