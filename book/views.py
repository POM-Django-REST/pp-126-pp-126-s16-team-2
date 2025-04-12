from django.shortcuts import render, redirect, get_object_or_404 
from .models import Book
from author.models import Author
from rest_framework import generics
from .serializers import BookSerializer


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
        new_author_name = request.POST.get("new_author")

        print(f"Створюємо книгу: {name}, опис: {description}, кількість: {count}, автори: {author_ids}, новий автор: {new_author_name}")

        book = Book.objects.create(
            name=name,
            description=description,
            count=count
        )

        if author_ids:
            book.authors.set(author_ids)

        if new_author_name:
            new_author, created = Author.objects.get_or_create(name=new_author_name)
            book.authors.add(new_author)

        return redirect('book_list')

    authors = Author.objects.all()
    return render(request, 'book/create.html', {'authors': authors})


def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    authors = Author.objects.all()

    if request.method == "POST":
        book.name = request.POST.get("name")
        book.description = request.POST.get("description")
        book.count = request.POST.get("count", 10)

        print(f"Редагування книги: {book.name}, автори: {book.authors.all()}")

        book.save()

        author_ids = request.POST.getlist("authors")
        book.authors.set(author_ids)

        print(f"Після редагування: {book.name}, автори: {book.authors.all()}")

        return redirect('book_list')

    return render(request, 'book/edit.html', {
        'book': book,
        'authors': authors
    })


def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        print(f"Видалення книги: {book.name}, автори: {book.authors.all()}")
        book.delete()
        return redirect('book_list')

    return render(request, 'book/confirm_delete.html', {'book': book})


def book_filter(request):
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


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
