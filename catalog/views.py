from django.shortcuts import render
from .data import get_all_books, get_book_by_id, get_books_count

def book_list(request):
    """Главная страница со списком всех книг."""
    books = get_all_books()
    context = {'books': books}
    return render(request, 'catalog/book_list.html', context)

def book_detail(request, book_id):
    """Страница с детальной информацией о книге."""
    book = get_book_by_id(book_id)
    if not book:
        # Если книга не найдена, показываем 404
        from django.http import Http404
        raise Http404("Книга не найдена")
    
    context = {'book': book}
    return render(request, 'catalog/book_detail.html', context)

def statistics(request):
    """Страница со статистикой."""
    book_count = get_books_count()
    context = {'book_count': book_count}
    return render(request, 'catalog/statistics.html', context)