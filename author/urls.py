from django.urls import path
from .views import author_list, author_create, author_delete, author_edit, author_books, AuthorDetailView, AuthorCreateView

urlpatterns = [
    path('', author_list, name='author_list'),
    path('create/', author_create, name='author_create'),
    path('<int:author_id>/delete/', author_delete, name='author_delete'),
    path('<int:author_id>/edit/', author_edit, name='author_edit'),
    path('<int:author_id>/books/', author_books, name='author_books'),
    path('api/v1/author/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    path('api/v1/author/create/', AuthorCreateView.as_view(), name='author-create'),
]
