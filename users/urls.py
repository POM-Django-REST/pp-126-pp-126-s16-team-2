from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list_view, name='user_list'),  # Список користувачів
    path('<int:user_id>/', views.user_detail_view, name='user_detail'),  # Детальна інформація про користувача
]

