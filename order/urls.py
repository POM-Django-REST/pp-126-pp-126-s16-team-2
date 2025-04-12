from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order-list'),                     # Для адміністраторів
    path('my-orders/', views.my_orders_view, name='my_orders'),       # ДЛЯ звичайного користувача
    path('create/', views.order_create, name='order-create'),
    path('<int:pk>/', views.order_detail, name='order-detail'),
    path('<int:pk>/edit/', views.order_edit, name='order-edit'),
]



