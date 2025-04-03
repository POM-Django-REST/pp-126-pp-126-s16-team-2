from django.db import models
from django.conf import settings  # Використання AUTH_USER_MODEL
from author.models import Author
import random  # Імпорт random для тестових даних


class Book(models.Model):
    name = models.CharField(max_length=128, blank=True)
    description = models.TextField(max_length=256, blank=True)
    count = models.IntegerField(default=10)
    authors = models.ManyToManyField('author.Author', related_name='book_authors', blank=True)  # Додано blank=True
    id = models.AutoField(primary_key=True)
    borrowed_books = models.IntegerField(default=0)

    class Meta:
        permissions = [
            ("can_view_books", "Can view books"),
            ("can_edit_books", "Can edit books"),
        ]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Book(id={self.id}, name={self.name})"

    @staticmethod
    def get_by_id(book_id):
        return Book.objects.filter(id=book_id).first()

    @staticmethod
    def delete_by_id(book_id):
        book = Book.get_by_id(book_id)
        if book:
            book.delete()
            return True
        return False

    @staticmethod
    def create(name, description, count=10, authors=None):
        if len(name) > 128:
            return None

        book = Book.objects.create(name=name, description=description, count=count)
        if authors:
            for author in authors:
                book.authors.add(author)
        return book

    @staticmethod
    def filter_books(name=None, author_id=None, count_min=None, count_max=None):
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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'count': self.count,
            'authors': [author.to_dict() for author in self.authors.all()]
        }

    def update(self, name=None, description=None, count=None):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if count is not None:
            self.count = count
        self.save()

    def add_authors(self, authors):
        if authors:
            for author in authors:
                self.authors.add(author)

    def remove_authors(self, authors):
        if authors:
            for author in authors:
                self.authors.remove(author)

    def borrow_book(self):
        if self.available_books > 0:
            self.borrowed_books += 1
            self.save()
        else:
            raise ValueError("No available copies to borrow.")

    @staticmethod
    def get_all():
        return list(Book.objects.all())

    def get_available_count(self):
        return self.count - self.borrowed_books

    @staticmethod
    def generate_test_data(num=10):
        for _ in range(num):
            name = f"Book {random.randint(1, 1000)}"
            description = f"Description {random.randint(1, 1000)}"
            count = random.randint(1, 50)
            book = Book.objects.create(name=name, description=description, count=count)

            authors = list(Author.objects.all())
            if authors:
                random_authors = random.sample(authors, min(len(authors), random.randint(1, 3)))
                book.authors.set(random_authors)

    @property
    def available_books(self):
        return self.count - self.borrowed_books


class LibraryMember(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='library_member')
    borrowed_books = models.ManyToManyField(Book, through='BorrowedBook', related_name='borrowed_by_members')

    def __str__(self):
        return f"{self.user.email} ({self.user.first_name} {self.user.last_name})"

    def __repr__(self):
        return f"LibraryMember(user={self.user.email})"


class BorrowedBook(models.Model):
    member = models.ForeignKey(LibraryMember, on_delete=models.CASCADE, related_name='borrowed_entries')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.book.name} (x{self.quantity}) - {self.member.user.email}"

    def __repr__(self):
        return f"BorrowedBook(book={self.book.name}, member={self.member.user.email}, quantity={self.quantity})"
