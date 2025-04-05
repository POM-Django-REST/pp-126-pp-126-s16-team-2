from django.shortcuts import render, get_object_or_404, redirect
from users.models import User
from users.forms import UserForm
from book.models import Book


def user_list_view(request):
    """Відображає список всіх користувачів."""
    users = User.objects.all()  # Отримання всіх користувачів
    return render(request, "users/user_list.html", {"users": users})


def user_detail_view(request, user_id):
    """Відображає деталі конкретного користувача."""
    user = get_object_or_404(User, id=user_id)
    viewed_books = user.viewed_books.all() if hasattr(user, 'viewed_books') else []  # Переглянуті книги
    borrowed_books = user.library_member.borrowed_books.all() if hasattr(user, 'library_member') else []  # Взяті книги
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
            form.save()  # Збереження нового користувача
            return redirect('user_list')  # Перенаправлення на список користувачів
    else:
        form = UserForm()
    return render(request, "users/add_user.html", {"form": form})


def edit_user(request, user_id):
    """Редагує існуючого користувача."""
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Зберігаємо оновлені дані користувача
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

        # Логування взаємодії
        print(f"Перед додаванням: {book.viewed_by_users.all()}")

        book.viewed_by_users.add(user)  # Додаємо користувача до ManyToManyField

        # Логування після взаємодії
        print(f"Після додавання: {book.viewed_by_users.all()}")

        return redirect('user_detail', user_id=user_id)

    return render(request, "users/user_books.html", {"user": user, "books": books})
