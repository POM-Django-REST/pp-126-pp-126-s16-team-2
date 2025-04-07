from django.shortcuts import render, redirect
from .models import Author
from .forms import AuthorForm
from django.shortcuts import get_object_or_404
from book.models import Book

def author_list(request):
    authors = Author.objects.prefetch_related('books').all()
    return render(request, 'author/list.html', {'authors': authors})


def author_create(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("author_list")
    else:
        form = AuthorForm()
    return render(request, "author/create.html", {"form": form})

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
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect("author_list")
    else:
        form = AuthorForm(instance=author)
    return render(request, "author/edit.html", {"form": form})


def author_books(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    books = author.books.all()
    return render(request, 'author/author_books.html', {
        'author': author,
        'books': books
    })