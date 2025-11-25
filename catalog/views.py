from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Min, Max
from .models import Book, Author, Genre, Review
from .forms import BookCreateForm, BookEditForm, ReviewForm, AuthorForm

def book_list(request):
    """Главная страница со списком всех книг из БД"""
    books = Book.objects.all().select_related('author').prefetch_related('genres')
    
    # Добавляем фильтрацию по жанру
    genre_id = request.GET.get('genre')
    if genre_id:
        books = books.filter(genres__id=genre_id)
    
    # Добавляем поиск
    search_query = request.GET.get('search')
    if search_query:
        books = books.filter(title__icontains=search_query)
    
    genres = Genre.objects.all()
    
    context = {
        'books': books,
        'genres': genres,
    }
    return render(request, 'catalog/book_list.html', context)

def book_detail(request, pk):
    """Страница с детальной информацией о книге"""
    book = get_object_or_404(Book.objects.select_related('author').prefetch_related('genres'), pk=pk)
    reviews = book.review_set.all().select_related('user')  # Это должно работать
    
    print(f"Найдено рецензий: {reviews.count()}")  # Для отладки
    
    context = {
        'book': book,
        'reviews': reviews,
    }
    return render(request, 'catalog/book_detail.html', context)

def statistics(request):
    """Страница со статистикой из реальной БД"""
    book_count = Book.objects.count()
    
    # Получаем реальную статистику из базы данных
    if book_count > 0:
        publication_years = Book.objects.aggregate(
            oldest=Min('publication_year'),
            newest=Max('publication_year')
        )
        
        # Самый популярный жанр
        popular_genre = Genre.objects.annotate(
            book_count=Count('book')
        ).order_by('-book_count').first()
        
        oldest_year = publication_years['oldest']
        newest_year = publication_years['newest']
        popular_genre_name = popular_genre.name if popular_genre else "Нет данных"
    else:
        oldest_year = newest_year = popular_genre_name = "Нет данных"
    
    context = {
        'book_count': book_count,
        'oldest_year': oldest_year,
        'newest_year': newest_year,
        'popular_genre': popular_genre_name,
    }
    return render(request, 'catalog/statistics.html', context)

@login_required
def create_book(request):
    """Создание новой книги (только для авторизованных пользователей)"""
    if request.method == 'POST':
        form = BookCreateForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Книга "{book.title}" успешно добавлена!')
            return redirect('book_detail', pk=book.pk)
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
            return redirect('book_list')
    else:
        form = AuthorForm()
    
    return render(request, 'catalog/author_form.html', {
        'form': form,
        'title': 'Добавить нового автора',
        'button_text': 'Добавить автора'
    })

@login_required
def delete_book(request, pk):
    """Удаление книги"""
    book = get_object_or_404(Book, pk=pk)
    title = book.title
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, f'Книга "{title}" успешно удалена!')
        return redirect('book_list')
    
    return render(request, 'catalog/confirm_delete.html', {'book': book})
def statistics(request):
    """Страница со статистикой из реальной БД"""
    # Основная статистика
    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    total_genres = Genre.objects.count()
    total_reviews = Review.objects.count()
    
    # Статистика по жанрам
    popular_genre = Genre.objects.annotate(
        book_count=Count('book')
    ).order_by('-book_count').first()
    
    # Статистика по годам
    publication_stats = Book.objects.aggregate(
        oldest_year=Min('publication_year'),
        newest_year=Max('publication_year'),
        avg_year=Avg('publication_year')
    )
    
    # Статистика по рейтингам
    rating_stats = Review.objects.aggregate(
        avg_rating=Avg('rating'),
        total_ratings=Count('id')
    )
    
    # Последние добавленные книги
    recent_books = Book.objects.select_related('author').order_by('-created_at')[:5]
    
    # Самые рецензируемые книги
    popular_books = Book.objects.annotate(
        review_count=Count('review')
    ).order_by('-review_count')[:3]
    
    # Все жанры для фильтра
    all_genres = Genre.objects.all()
    
    context = {
        'total_books': total_books,
        'total_authors': total_authors,
        'total_genres': total_genres,
        'total_reviews': total_reviews,
        'popular_genre': popular_genre,
        'popular_genre_count': popular_genre.book_count if popular_genre else 0,
        'oldest_year': publication_stats['oldest_year'],
        'newest_year': publication_stats['newest_year'],
        'avg_publication_year': round(publication_stats['avg_year']) if publication_stats['avg_year'] else 0,
        'avg_rating': round(rating_stats['avg_rating'], 1) if rating_stats['avg_rating'] else 0,
        'total_ratings': rating_stats['total_ratings'],
        'recent_books': recent_books,
        'popular_books': popular_books,
        'genres': all_genres,
    }
    return render(request, 'catalog/statistics.html', context)
def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно! Добро пожаловать в библиотеку!')
            return redirect('book_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

# Остальные функции остаются без изменений, но добавляем декоратор @login_required

@login_required
def create_book(request):
    """Создание новой книги (только для авторизованных пользователей)"""
    if request.method == 'POST':
        form = BookCreateForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Книга "{book.title}" успешно добавлена!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookCreateForm()
    
    return render(request, 'catalog/book_form.html', {
        'form': form,
        'title': 'Добавить новую книгу',
        'button_text': 'Добавить книгу'
    })

@login_required
def edit_book(request, pk):
    """Редактирование книги (только для авторизованных пользователей)"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookEditForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'Изменения в книге "{book.title}" успешно сохранены!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookEditForm(instance=book)
    
    return render(request, 'catalog/book_form.html', {
        'form': form,
        'title': f'Редактировать книгу: {book.title}',
        'button_text': 'Сохранить изменения'
    })

@login_required
def add_review(request, pk):
    """Добавление рецензии (только для авторизованных пользователей)"""
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
    """Создание нового автора (только для авторизованных пользователей)"""
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            messages.success(request, f'Автор "{author.name}" успешно добавлен!')
            return redirect('book_list')
    else:
        form = AuthorForm()
    
    return render(request, 'catalog/author_form.html', {
        'form': form,
        'title': 'Добавить нового автора',
        'button_text': 'Добавить автора'
    })

@login_required
def delete_book(request, pk):
    """Удаление книги (только для авторизованных пользователей)"""
    book = get_object_or_404(Book, pk=pk)
    title = book.title
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, f'Книга "{title}" успешно удалена!')
        return redirect('book_list')
    
    return render(request, 'catalog/confirm_delete.html', {'book': book})