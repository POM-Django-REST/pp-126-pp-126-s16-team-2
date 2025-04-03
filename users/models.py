from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class User(AbstractUser):
    # Кількість переглянутих книг
    viewed_books = models.IntegerField(default=0, verbose_name="Переглянуті книги")
    # Кількість взятих книг
    borrowed_books = models.IntegerField(default=0, verbose_name="Взяті книги")
    # Кількість повернутих книг
    returned_books = models.IntegerField(default=0, verbose_name="Повернуті книги")
    # Зв'язок із моделлю Book
    books = models.ManyToManyField(
        'book.Book',
        blank=True,
        related_name="users",  # Додаємо related_name для чіткості зв'язків
        verbose_name="Книги"
    )
    # Дата створення профілю
    created_at = models.DateTimeField(default=now, verbose_name="Дата створення")
    # Дата оновлення профілю
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    # Роль користувача (наприклад, звичайний користувач чи адміністратор)
    role = models.CharField(max_length=50, default="visitor", verbose_name="Роль")

    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"

    def __str__(self):
        return f"{self.username} ({self.role})"  # Відображення username та ролі для моделі User

    def get_full_name(self):
        """Метод повертає повне ім'я користувача."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_borrowed_books_count(self):
        """Метод повертає кількість взятих книг."""
        return self.borrowed_books

    def get_returned_books_count(self):
        """Метод повертає кількість повернутих книг."""
        return self.returned_books
