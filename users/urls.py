from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list_view, name='user_list'),  # Список користувачів
    path('<int:user_id>/', views.user_detail_view, name='user_detail'),  # Детальна інформація про користувача
    path('add/', views.add_user, name='add_user'),  # Додавання нового користувача
    path('<int:user_id>/edit/', views.edit_user, name='edit_user'),  # Редагування користувача
    path('<int:user_id>/books/', views.user_book_interaction, name='user_books'),  # Взаємодія з книгами
]
