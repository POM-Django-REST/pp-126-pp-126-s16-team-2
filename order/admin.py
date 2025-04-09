from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'created_at', 'plated_end_at')
    list_filter = ('created_at', 'plated_end_at')
    search_fields = ('user__username', 'book__title')