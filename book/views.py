from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from author.models import Author


def book_list(request):
    """Відображає список всіх книг із попередньо завантаженими авторами."""
    books = Book.objects.all().prefetch_related('authors')
    return render(request, 'book/list.html', {'books': books})


def book_detail(request, book_id):
    """Відображає деталі конкретної книги."""
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book/detail.html', {'book': book})


def book_create(request):
    """Створює нову книгу."""
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        count = request.POST.get("count", 10)
        author_ids = request.POST.getlist("authors")
<<<<<<< HEAD
        new_author_name = request.POST.get("new_author")

        # Логування для перевірки даних
        print(f"Створюємо книгу: {name}, опис: {description}, кількість: {count}, автори: {author_ids}, новий автор: {new_author_name}")

        # Створення книги
=======

        # Логування для перевірки даних
        print(f"Створюємо книгу: {name}, опис: {description}, кількість: {count}, автори: {author_ids}")

>>>>>>> Daniil
        book = Book.objects.create(
            name=name,
            description=description,
            count=count
        )

<<<<<<< HEAD
        # Додавання існуючих авторів
        if author_ids:
            book.authors.set(author_ids)

        # Створення нового автора та додавання його до книги
        if new_author_name:
            new_author, created = Author.objects.get_or_create(name=new_author_name)
            book.authors.add(new_author)

        return redirect('book_list')  # Повернення до списку книг
=======
        if author_ids:
            book.authors.set(author_ids)

        return redirect('book_detail', book_id=book.id)
>>>>>>> Daniil

    authors = Author.objects.all()
    return render(request, 'book/create.html', {'authors': authors})


def book_edit(request, book_id):
    """Редагує існуючу книгу."""
    book = get_object_or_404(Book, id=book_id)
    authors = Author.objects.all()

    if request.method == "POST":
        book.name = request.POST.get("name")
        book.description = request.POST.get("description")
        book.count = request.POST.get("count", 10)

        # Логування перед збереженням
        print(f"Редагування книги: {book.name}, автори: {book.authors.all()}")

        book.save()

        author_ids = request.POST.getlist("authors")
        book.authors.set(author_ids)

        # Логування після збереження
        print(f"Після редагування: {book.name}, автори: {book.authors.all()}")

<<<<<<< HEAD
        return redirect('book_list')  # Повернення до списку книг
=======
        return redirect('book_detail', book_id=book.id)
>>>>>>> Daniil

    return render(request, 'book/edit.html', {
        'book': book,
        'authors': authors
    })


def book_delete(request, book_id):
    """Видаляє книгу."""
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        # Логування перед видаленням
        print(f"Видалення книги: {book.name}, автори: {book.authors.all()}")

        book.delete()
<<<<<<< HEAD
        return redirect('book_list')  # Повернення до списку книг
=======
        return redirect('book_list')
>>>>>>> Daniil

    return render(request, 'book/confirm_delete.html', {'book': book})


def book_filter(request):
    """Фільтрує книги за назвою або автором."""
    books = Book.objects.all()

    name = request.GET.get('name')
    if name:
        books = books.filter(name__icontains=name)

    author_id = request.GET.get('author')
    if author_id:
        books = books.filter(authors__id=author_id)

    authors = Author.objects.all()
    return render(request, 'book/filter.html', {
        'books': books,
        'authors': authors,
        'search_params': request.GET
    })
<<<<<<< HEAD

from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

=======
>>>>>>> Daniil
