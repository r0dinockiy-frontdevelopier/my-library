from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя автора")
    bio = models.TextField(blank=True, verbose_name="Биография")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('author_detail', kwargs={'pk': self.pk})
    
    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название жанра")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    genres = models.ManyToManyField(Genre, verbose_name="Жанры")
    publication_year = models.IntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(2030)],
        verbose_name="Год издания"
    )
    annotation = models.TextField(verbose_name="Аннотация")
    cover = models.ImageField(upload_to='covers/', blank=True, verbose_name="Обложка")
    pages = models.IntegerField(default=0, verbose_name="Количество страниц")
    isbn = models.CharField(max_length=13, blank=True, verbose_name="ISBN")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    def __str__(self):
        return f"{self.title} - {self.author.name}"
    
    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.pk})
    
    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['-created_at']

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Рейтинг"
    )
    text = models.TextField(verbose_name="Текст рецензии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    def __str__(self):
        return f"Рецензия на {self.book.title} от {self.user.username}"
    
    class Meta:
        verbose_name = "Рецензия"
        verbose_name_plural = "Рецензии"
        unique_together = ['book', 'user']
        ordering = ['-created_at']