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
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg
from .models import Book, Review, Author, Genre
from .forms import BookCreateForm, BookEditForm, ReviewForm, AuthorForm

def book_list(request):
    """Главная страница со списком всех книг из БД"""
    books = Book.objects.all().select_related('author').prefetch_related('genres')
    
    # Фильтрация по жанру
    genre_filter = request.GET.get('genre')
    if genre_filter:
        books = books.filter(genres__id=genre_filter)
    
    # Поиск
    search_query = request.GET.get('search')
    if search_query:
        books = books.filter(title__icontains=search_query)
    
    genres = Genre.objects.all()
    
    context = {
        'books': books,
        'genres': genres,
        'current_genre': genre_filter,
        'search_query': search_query or ''
    }
    return render(request, 'catalog/book_list.html', context)

def book_detail(request, pk):
    """Страница с детальной информацией о книге из БД"""
    book = get_object_or_404(
        Book.objects.select_related('author').prefetch_related('genres', 'review_set__user'), 
        pk=pk
    )
    reviews = book.review_set.all().select_related('user')
    
    # Средний рейтинг
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    # Форма для рецензии
    review_form = ReviewForm()
    
    context = {
        'book': book, 
        'reviews': reviews,
        'review_form': review_form,
        'avg_rating': avg_rating,
        'can_add_review': request.user.is_authenticated and not reviews.filter(user=request.user).exists()
    }
    return render(request, 'catalog/book_detail.html', context)

@login_required
def create_book(request):
    """Создание новой книги"""
    if request.method == 'POST':
        form = BookCreateForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Книга "{book.title}" успешно добавлена в библиотеку!')
            return redirect('book_detail', pk=book.pk)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = BookCreateForm()
    
    return render(request, 'catalog/book_form.html', {
        'form': form,
        'title': 'Добавить новую книгу',
        'button_text': 'Добавить книгу'
    })

@login_required
def edit_book(request, pk):
    """Редактирование книги"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookEditForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'Изменения в книге "{book.title}" успешно сохранены!')
            return redirect('book_detail', pk=book.pk)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = BookEditForm(instance=book)
    
    return render(request, 'catalog/book_form.html', {
        'form': form,
        'title': f'Редактировать книгу: {book.title}',
        'button_text': 'Сохранить изменения'
    })

@login_required
def add_review(request, pk):
    """Добавление рецензии"""
    book = get_object_or_404(Book, pk=pk)
    
    # Проверяем, есть ли уже рецензия от этого пользователя
    existing_review = Review.objects.filter(book=book, user=request.user).first()
    
    if request.method == 'POST':
        if existing_review:
            form = ReviewForm(request.POST, instance=existing_review)
        else:
            form = ReviewForm(request.POST)
        
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, 'Ваша рецензия успешно добавлена!')
            return redirect('book_detail', pk=book.pk)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        if existing_review:
            form = ReviewForm(instance=existing_review)
        else:
            form = ReviewForm()
    
    return render(request, 'catalog/review_form.html', {
        'form': form,
        'book': book,
        'existing_review': existing_review
    })

@login_required
def create_author(request):
    """Создание нового автора"""
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            messages.success(request, f'Автор "{author.name}" успешно добавлен!')
            return redirect('book_list')  # или на страницу автора
    else:
        form = AuthorForm()
    
    return render(request, 'catalog/author_form.html', {
        'form': form,
        'title': 'Добавить нового автора',
        'button_text': 'Добавить автора'
    })

def statistics(request):
    """Страница со статистикой из БД"""
    book_count = Book.objects.count()
    author_count = Author.objects.count()
    genre_count = Genre.objects.count()
    review_count = Review.objects.count()
    
    # Самые популярные жанры
    popular_genres = Genre.objects.annotate(
        book_count=Count('book')
    ).order_by('-book_count')[:5]
    
    # Книги с лучшим рейтингом
    top_rated_books = Book.objects.annotate(
        avg_rating=Avg('review__rating')
    ).filter(avg_rating__isnull=False).order_by('-avg_rating')[:5]
    
    context = {
        'book_count': book_count,
        'author_count': author_count,
        'genre_count': genre_count,
        'review_count': review_count,
        'popular_genres': popular_genres,
        'top_rated_books': top_rated_books,
    }
    return render(request, 'catalog/statistics.html', context)