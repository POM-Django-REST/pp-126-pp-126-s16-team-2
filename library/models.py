from django.db import models
from django.conf import settings  # Імпорт налаштувань
from book.models import Book  # Імпорт моделей книги

class LibraryMember(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Використання AUTH_USER_MODEL
        on_delete=models.CASCADE,
        related_name="library_member"
    )
    borrowed_books = models.ManyToManyField(
        Book,
        through='BorrowedBook',
        related_name="borrowed_by_members"
    )

    def __str__(self):
        return f"{self.user.username} ({self.user.email})"

class BorrowedBook(models.Model):
    member = models.ForeignKey(
        LibraryMember,
        on_delete=models.CASCADE,
        related_name="borrowed_entries"  # Змінено related_name для уникнення конфліктів
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )
    borrow_date = models.DateField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.book.name} (x{self.quantity}) - {self.member.user.username}"
