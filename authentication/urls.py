from django.urls import path
from .views import (
    register_view, login_view, logout_view,
    user_list_view, user_detail_view, my_orders_view
)
from authentication.custom_admin import custom_admin_site

urlpatterns = [
    path("register/", register_view, name="register"),  # Реєстрація
    path("login/", login_view, name="login"),  # Авторизація
    path("logout/", logout_view, name="logout"),  # Вихід з системи
    path("users/", user_list_view, name="user_list"),  # Список користувачів
    path("users/<int:user_id>/", user_detail_view, name="user_detail"),  # Деталі користувача
    path("my-orders/", my_orders_view, name="my_orders"),  # Замовлення користувача
    path('admin/', custom_admin_site.urls),  # Кастомна адмін-панель
]


