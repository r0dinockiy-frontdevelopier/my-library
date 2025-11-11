from django import forms
from django.core.exceptions import ValidationError
from .models import Book, Author, Genre, Review
from django.contrib.auth.models import User

class BookCreateForm(forms.ModelForm):
    """Форма для создания новой книги"""
    class Meta:
        model = Book
        fields = ['title', 'author', 'genres', 'publication_year', 'annotation', 'cover', 'pages', 'isbn']
        widgets = {
            'genres': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-select-multiple'}),
            'annotation': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Введите аннотацию книги...'}),
            'publication_year': forms.NumberInput(attrs={'min': 1000, 'max': 2030}),
            'title': forms.TextInput(attrs={'placeholder': 'Название книги'}),
        }
        labels = {
            'title': 'Название книги',
            'author': 'Автор',
            'genres': 'Жанры',
            'publication_year': 'Год издания',
            'annotation': 'Аннотация',
            'cover': 'Обложка',
            'pages': 'Количество страниц',
            'isbn': 'ISBN',
        }
    
    def clean_title(self):
        """Проверка названия книги"""
        title = self.cleaned_data['title']
        if len(title) < 2:
            raise ValidationError('Название книги слишком короткое. Минимум 2 символа.')
        if len(title) > 200:
            raise ValidationError('Название книги слишком длинное. Максимум 200 символов.')
        return title
    
    def clean_publication_year(self):
        """Проверка года издания"""
        year = self.cleaned_data['publication_year']
        if year < 1000 or year > 2030:
            raise ValidationError('Некорректный год издания. Допустимый диапазон: 1000-2030.')
        return year
    
    def clean_pages(self):
        """Проверка количества страниц"""
        pages = self.cleaned_data['pages']
        if pages < 0:
            raise ValidationError('Количество страниц не может быть отрицательным.')
        return pages

class BookEditForm(forms.ModelForm):
    """Форма для редактирования книги"""
    class Meta:
        model = Book
        fields = ['title', 'author', 'genres', 'publication_year', 'annotation', 'cover', 'pages', 'isbn']
        widgets = {
            'genres': forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-select-multiple'}),
            'annotation': forms.Textarea(attrs={'rows': 4}),
            'publication_year': forms.NumberInput(attrs={'min': 1000, 'max': 2030}),
        }

class ReviewForm(forms.ModelForm):
    """Форма для добавления рецензии"""
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Напишите вашу рецензию...',
                'class': 'review-textarea'
            }),
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
        }
        labels = {
            'rating': 'Оценка (1-5)',
            'text': 'Текст рецензии',
        }
    
    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise ValidationError('Рейтинг должен быть от 1 до 5.')
        return rating
    
    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text.strip()) < 10:
            raise ValidationError('Рецензия должна содержать минимум 10 символов.')
        return text

class AuthorForm(forms.ModelForm):
    """Форма для автора"""
    class Meta:
        model = Author
        fields = ['name', 'bio', 'birth_date']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }