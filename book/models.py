from django.db import models
from author.models import Author
from django.contrib.auth import get_user_model
import random

User = get_user_model()


class Book(models.Model):
    title = models.CharField(max_length=255, default="Default Title")

    borrowed_by_users = models.ManyToManyField(
        User, related_name='borrowed_books', blank=True
    )
    viewed_by_users = models.ManyToManyField(
        User, related_name='viewed_books', blank=True
    )
    name = models.CharField(max_length=128, blank=True)
    description = models.TextField(max_length=256, blank=True)
    count = models.IntegerField(default=10)
    authors = models.ManyToManyField(
        Author, related_name='book_authors', blank=True
    )
    id = models.AutoField(primary_key=True)

    class Meta:
        permissions = [
            ("can_view_books", "Can view books"),
            ("can_edit_books", "Can edit books"),
        ]

    def __str__(self):
        return self.name or self.title

    def add_viewed_user(self, user):
        """Додає одного користувача до списку тих, хто переглянув книгу."""
        if user not in self.viewed_by_users.all():
            self.viewed_by_users.add(user)

    def add_borrowed_user(self, user):
        """Додає одного користувача до списку тих, хто взяв книгу."""
        if user not in self.borrowed_by_users.all():
            self.borrowed_by_users.add(user)

    def set_viewed_users(self, user_list):
        """Оновлює список користувачів, які переглянули книгу."""
        self.viewed_by_users.set(user_list)

    def set_borrowed_users(self, user_list):
        """Оновлює список користувачів, які взяли книгу."""
        self.borrowed_by_users.set(user_list)

    @staticmethod
    def get_by_id(book_id):
        """Отримує книгу за ID."""
        return Book.objects.filter(id=book_id).first()

    @staticmethod
    def delete_by_id(book_id):
        """Видаляє книгу за ID."""
        book = Book.get_by_id(book_id)
        if book:
            book.delete()
            return True
        return False

    @staticmethod
    def create(name, description, count=10, authors=None):
        """Створює нову книгу."""
        if len(name) > 128:
            return None

        book = Book.objects.create(
            name=name, description=description, count=count
        )
        if authors:
            book.authors.set(authors)
        return book

    @staticmethod
    def filter_books(name=None, author_id=None, count_min=None, count_max=None):
        """Фільтрує книги за різними критеріями."""
        books = Book.objects.all()
        if name:
            books = books.filter(name__icontains=name)
        if author_id:
            books = books.filter(authors__id=author_id)
        if count_min is not None:
            books = books.filter(count__gte=count_min)
        if count_max is not None:
            books = books.filter(count__lte=count_max)
        return books

    @property
    def available_books(self):
        """Повертає кількість доступних книг."""
        return self.count - self.borrowed_by_users.count()

    @staticmethod
    def generate_test_data(num=10):
        """Генерує тестові дані для книг."""
        for _ in range(num):
            name = f"Book {random.randint(1, 1000)}"
            description = f"Description {random.randint(1, 1000)}"
            count = random.randint(1, 50)
            book = Book.objects.create(
                name=name, description=description, count=count
            )

            authors = list(Author.objects.all())
            if authors:
                random_authors = random.sample(
                    authors, min(len(authors), random.randint(1, 3))
                )
                book.authors.set(random_authors)


class LibraryMember(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='library_member'
    )
    borrowed_books = models.ManyToManyField(
        Book, through='BorrowedBook', related_name='borrowed_by_members'
    )

    def __str__(self):
        return f"{self.user.email} ({self.user.first_name} {self.user.last_name})"


class BorrowedBook(models.Model):
    member = models.ForeignKey(
        LibraryMember, on_delete=models.CASCADE, related_name='borrowed_entries'
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.book.name} (x{self.quantity}) - {self.member.user.email}"
