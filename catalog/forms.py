from django import forms
from django.core.exceptions import ValidationError
from .models import Book, Author, Genre, Review

class BookCreateForm(forms.ModelForm):
    """Форма для создания новой книги"""
    class Meta:
        model = Book
        fields = ['title', 'author', 'genres', 'publication_year', 'annotation', 'cover', 'pages', 'isbn']
        widgets = {
            'genres': forms.CheckboxSelectMultiple,
            'annotation': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean_title(self):
        """Проверка названия книги"""
        title = self.cleaned_data['title']
        if len(title) < 2:
            raise ValidationError('Название книги слишком короткое.')
        return title

class BookEditForm(forms.ModelForm):
    """Форма для редактирования книги"""
    class Meta:
        model = Book
        fields = ['title', 'author', 'genres', 'publication_year', 'annotation', 'cover', 'pages', 'isbn']
        widgets = {
            'genres': forms.CheckboxSelectMultiple,
            'annotation': forms.Textarea(attrs={'rows': 4}),
        }

class ReviewForm(forms.ModelForm):
    """Форма для добавления рецензии"""
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Напишите вашу рецензию...'}),
        }
    
    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise ValidationError('Рейтинг должен быть от 1 до 5.')
        return rating

class AuthorForm(forms.ModelForm):
    """Форма для автора"""
    class Meta:
        model = Author
        fields = ['name', 'bio', 'birth_date']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }