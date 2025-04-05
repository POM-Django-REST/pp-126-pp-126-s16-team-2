from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    """Розширена модель користувача."""
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
        """Повертає рядкове представлення моделі користувача."""
        return f"{self.username} ({self.role})"

    def get_full_name(self):
        """Метод повертає повне ім'я користувача."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_viewed_books_count(self):
        """Метод повертає кількість переглянутих книг."""
        # Оновлено для обробки зв’язків через related_name
        return self.viewed_books.count()

    def get_borrowed_books_count(self):
        """Метод повертає кількість взятих книг."""
        return self.borrowed_books.count()

    def get_returned_books_count(self):
        """Метод повертає кількість повернутих книг."""
        # Уточнено для додаткової логіки
        # Якщо в моделі Book є поле returned, переконайтеся, що вона правильно налаштована
        return self.books.filter(returned=True).count()
