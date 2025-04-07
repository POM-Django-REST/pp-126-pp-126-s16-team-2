from django.contrib import admin
from .models import Author

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'patronymic')  # Відображення імені, прізвища та по-батькові
    search_fields = ('name', 'surname')  # Пошук за іменем та прізвищем
    list_filter = ('surname',)  # Фільтр за прізвищем

admin.site.register(Author, AuthorAdmin)
