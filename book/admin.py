from django.contrib import admin
from .models import Book, BorrowedBook, LibraryMember
from .forms import BookForm

# Кастомна адмінка для моделі Book
class BookAdmin(admin.ModelAdmin):
    form = BookForm  # Підключаємо кастомну форму
    list_display = ('name', 'description', 'count', 'get_borrowed_books_count', 'display_authors')
    list_filter = ('count', 'authors', 'name')
    search_fields = ('name', 'description')
    filter_horizontal = ('authors',)  # Горизонтальне редагування ManyToMany поля

    def get_borrowed_books_count(self, obj):
        """Повертає кількість користувачів, які взяли книгу."""
        return obj.borrowed_by_users.count()
    get_borrowed_books_count.short_description = 'Взяті книги'

    def display_authors(self, obj):
        """Відображає список авторів через кому."""
        return ", ".join([author.surname for author in obj.authors.all()])
    display_authors.short_description = 'Authors'  # Назва колонки

# Кастомна адмінка для моделі LibraryMember
class LibraryMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_borrowed_books')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')

    def display_borrowed_books(self, obj):
        """Відображає список книг, взятих користувачем через кому."""
        return ", ".join([book.name for book in obj.borrowed_books.all()])
    display_borrowed_books.short_description = 'Borrowed Books'

# Кастомна адмінка для моделі BorrowedBook
class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ('member', 'book', 'borrow_date', 'quantity')
    search_fields = ('member__user__email', 'book__name')
    list_filter = ('borrow_date',)

# Реєстрація моделей у адмінці
admin.site.register(Book, BookAdmin)
admin.site.register(LibraryMember, LibraryMemberAdmin)
admin.site.register(BorrowedBook, BorrowedBookAdmin)





