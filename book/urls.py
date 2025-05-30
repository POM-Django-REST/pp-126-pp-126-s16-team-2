from django.urls import path
from .views import book_list, book_detail, book_create, book_edit, book_delete, book_filter
from . import views
from .views import BookDetailView, BookCreateView


urlpatterns = [
    path('', book_list, name='book_list'),
    path('create/', book_create, name='book_create'),
    path('<int:book_id>/', book_detail, name='book_detail'),
    path('<int:book_id>/edit/', book_edit, name='book_edit'),
    path('<int:book_id>/delete/', book_delete, name='book_delete'),
    path('filter/', book_filter, name='book_filter'),

    # API (для Postman, REST, DRF)
    path('api/<int:pk>/', BookDetailView.as_view(), name='api-book-detail'),
    path('api/create/', BookCreateView.as_view(), name='api-book-create'),
]
