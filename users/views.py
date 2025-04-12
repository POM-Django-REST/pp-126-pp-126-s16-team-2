from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404, redirect
from .models import User
from .forms import UserForm
from .serializers import UserSerializer
from book.models import Book


def user_list_view(request):
    """Відображає список всіх користувачів."""
    users = User.objects.all()
    return render(request, "users/user_list.html", {"users": users})


def user_detail_view(request, user_id):
    """Відображає деталі конкретного користувача."""
    user = get_object_or_404(User, id=user_id)
    viewed_books = user.viewed_books.all() if hasattr(user, 'viewed_books') else []
    borrowed_books = user.borrowed_books.all() if hasattr(user, 'borrowed_books') else []
    return render(request, "users/user_detail.html", {
        "user": user,
        "viewed_books": viewed_books,
        "borrowed_books": borrowed_books
    })


def add_user(request):
    """Додає нового користувача."""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, "users/add_user.html", {"form": form})


def edit_user(request, user_id):
    """Редагує існуючого користувача."""
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'users/edit_user.html', {'form': form, 'user': user})


def user_book_interaction(request, user_id):
    """Додає логіку для взаємодії користувачів із книгами."""
    user = get_object_or_404(User, id=user_id)
    books = Book.objects.all()

    if request.method == 'POST':
        book_id = request.POST.get("book_id")
        book = get_object_or_404(Book, id=book_id)
        book.viewed_by_users.add(user)
        return redirect('user_detail', user_id=user_id)

    return render(request, "users/user_books.html", {"user": user, "books": books})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
