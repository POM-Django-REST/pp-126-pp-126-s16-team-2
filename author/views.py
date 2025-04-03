from django.shortcuts import render, redirect
from .models import Author
from django.shortcuts import get_object_or_404
from book.models import Book

def author_list(request):
    authors = Author.objects.prefetch_related('books').all()
    return render(request, 'author/list.html', {'authors': authors})


def author_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        Author.objects.create(name=name, surname=surname)
        return redirect("author_list")
    return render(request, "author/create.html")


def author_delete(request, author_id):
    author = get_object_or_404(Author, id=author_id)

    if author.books.exists():
        return render(request, 'author/delete_error.html', {'author': author})

    if request.method == "POST":
        author.delete()
        return redirect('author_list')

    return render(request, 'author/confirm_delete.html', {'author': author})


def author_edit(request, author_id):
    author = get_object_or_404(Author, id=author_id)

    if request.method == "POST":
        author.name = request.POST.get("name")
        author.surname = request.POST.get("surname")
        author.save()
        selected_books = request.POST.getlist("books")
        author.books.set(selected_books)
        return redirect("author_list")

    return render(request, "author/edit.html", {"author": author})


def author_edit(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    all_books = Book.objects.all()

    if request.method == "POST":
        author.name = request.POST.get("name")
        author.surname = request.POST.get("surname")
        author.save()
        selected_books = request.POST.getlist("books")
        author.books.set(selected_books)
        return redirect("author_list")

    return render(request, "author/edit.html", {
        "author": author,
        "all_books": all_books
    })

def author_books(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    books = author.books.all()
    return render(request, 'author/author_books.html', {
        'author': author,
        'books': books
    })