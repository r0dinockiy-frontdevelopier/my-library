class Book:
    def __init__(self, id, title, author, cover_path, annotation, genre, publication_year, review):
        self.id = id
        self.title = title
        self.author = author
        self.cover_path = cover_path  # путь к файлу обложки
        self.annotation = annotation
        self.genre = genre
        self.publication_year = publication_year
        self.review = review

# Создаем "базу данных" в памяти
books_data = [
    Book(
        id=1,
        title="Мастер и Маргарита",
        author="Михаил Булгаков",
        cover_path="covers/master.jpg",
        annotation="Великий роман о добре и зле, любви и творчестве.",
        genre="Роман",
        publication_year=1966,
        review="Один из величайших романов XX века. Перечитываю каждый год."
    ),
    Book(
        id=2,
        title="1984",
        author="Джордж Оруэлл",
        cover_path="covers/1984.jpg",
        annotation="Антиутопия о тоталитарном обществе будущего.",
        genre="Антиутопия",
        publication_year=1949,
        review="Пугающе актуально в наше время. Обязательно к прочтению."
    ),
    Book(
        id=3,
        title="Преступление и наказание",
        author="Федор Достоевский",
        cover_path="covers/crime.jpg",
        annotation="Психологический роман о преступлении и его последствиях.",
        genre="Психологический роман",
        publication_year=1866,
        review="Глубокое исследование человеческой души. Классика!"
    ),
]

def get_all_books():
    """Возвращает все книги"""
    return books_data

def get_book_by_id(book_id):
    """Находит книгу по ID"""
    for book in books_data:
        if book.id == book_id:
            return book
    return None

def get_books_count():
    """Возвращает количество книг"""
    return len(books_data)