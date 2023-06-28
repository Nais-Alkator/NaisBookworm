import sys
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

# Additionally remove the current file's directory from sys.path
try:
    sys.path.remove(str(parent))
except ValueError: # Already removed
    pass

from app import app
from models import db, Author, Book


authors_names = [
    "Дж. К. Роулинг",
    "Лев Толстой",
    "Уильям Шекспир",
    "Федор Достоевский",
    "Джордж Оруэлл",
    "Джейн Остин",
    "Чарльз Диккенс",
    "Эрнест Хемингуэй",
    "Агата Кристи",
    "Рэй Брэдбери"
]

books = [
    {"title": "Гарри Поттер и философский камень", "authors": ["Дж. К. Роулинг"]},
    {"title": "Война и мир", "authors": ["Лев Толстой"]},
    {"title": "Гамлет", "authors": ["Уильям Шекспир"]},
    {"title": "Преступление и наказание", "authors": ["Федор Достоевский"]},
    {"title": "1984", "authors": ["Джордж Оруэлл"]},
    {"title": "Гордость и предубеждение", "authors": ["Джейн Остин"]},
    {"title": "Оливер Твист", "authors": ["Чарльз Диккенс"]},
    {"title": "Старик и море", "authors": ["Эрнест Хемингуэй"]},
    {"title": "Убийство в Восточном экспрессе", "authors": ["Агата Кристи"]},
    {"title": "451 градус по Фаренгейту", "authors": ["Рэй Брэдбери"]}
]


def create_authors(author_names):
    authors = [Author(name=name) for name in author_names]
    db.session.add_all(authors)
    db.session.commit()


def create_book(title, author_names):
    book = Book(title=title)
    authors = []

    for author_name in author_names:
        author = Author.query.filter_by(name=author_name).first()
        if author:
            authors.append(author)
        else:
            new_author = Author(name=author_name)
            db.session.add(new_author)
            authors.append(new_author)

    book.authors = authors
    db.session.add(book)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        create_authors(authors_names)
        for book in books:
            create_book(book['title'], book['authors'])