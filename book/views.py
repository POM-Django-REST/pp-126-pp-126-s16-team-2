from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from author.models import Author


def book_list(request):
    books = Book.objects.all().prefetch_related('authors')
    return render(request, 'book/list.html', {'books': books})


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book/detail.html', {'book': book})


def book_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        count = request.POST.get("count", 10)
        author_ids = request.POST.getlist("authors")

        book = Book.objects.create(
            name=name,
            description=description,
            count=count
        )

        if author_ids:
            book.authors.set(author_ids)

        return redirect('book_detail', book_id=book.id)

    authors = Author.objects.all()
    return render(request, 'book/create.html', {'authors': authors})


def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    authors = Author.objects.all()

    if request.method == "POST":
        book.name = request.POST.get("name")
        book.description = request.POST.get("description")
        book.count = request.POST.get("count", 10)
        book.save()

        author_ids = request.POST.getlist("authors")
        book.authors.set(author_ids)

        return redirect('book_detail', book_id=book.id)

    return render(request, 'book/edit.html', {
        'book': book,
        'authors': authors
    })


def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        book.delete()
        return redirect('book_list')

    return render(request, 'book/confirm_delete.html', {'book': book})


def book_filter(request):
    books = Book.objects.all()

    # Filtering logic
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

def book_list(request):
    books = Book.objects.all()  # Отримуємо всі книги з бази даних
    return render(request, 'book_list.html', {'books': books})  # Рендеримо шаблон і передаємо дані
