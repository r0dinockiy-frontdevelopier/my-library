from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publication_year', 'pages', 'created_at']
    list_filter = ['author', 'genres', 'publication_year']
    search_fields = ['title', 'author__name', 'isbn']
    filter_horizontal = ['genres']  # Для удобного выбора жанров
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'author', 'genres', 'publication_year')
        }),
        ('Дополнительная информация', {
            'fields': ('annotation', 'cover', 'pages', 'isbn')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )