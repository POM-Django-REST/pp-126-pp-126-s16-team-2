from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from rest_framework.routers import DefaultRouter
from users import views as users_views
from order import views as order_views

# Тимчасова домашня сторінка
def temporary_home(request):
    return render(request, 'home.html')

# API router
router = DefaultRouter()
router.register(r'api/v1/user', users_views.UserViewSet, basename='user')
router.register(r'api/v1/order', order_views.OrderViewSet, basename='order')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("authentication/", include("authentication.urls")),
    path("orders/", include("order.urls")),
    path("authors/", include("author.urls")),
    path("books/", include("book.urls")),
    path("users/", include("users.urls")),
    path("", temporary_home, name="home"),

    # API endpoints
    path('api/v1/user/<int:user_id>/order/', order_views.UserOrderViewSet.as_view({'get': 'list'})),
    path('api/v1/user/<int:user_id>/order/<int:pk>/', order_views.OrderViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('', include(router.urls)),
]
