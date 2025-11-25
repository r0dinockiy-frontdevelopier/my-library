from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('statistics/', views.statistics, name='statistics'),
    
    # Защищенные маршруты (только для авторизованных пользователей)
    path('book/create/', views.create_book, name='create_book'),
    path('book/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:pk>/review/', views.add_review, name='add_review'),
    path('book/<int:pk>/delete/', views.delete_book, name='delete_book'),
    path('author/create/', views.create_author, name='create_author'),
]