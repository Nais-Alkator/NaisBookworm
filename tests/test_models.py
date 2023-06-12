import pytest
from models import Author, Book, User


@pytest.fixture
def sample_author(app, db):
    with app.app_context():
        author = Author(name="Антон Павлович Чехов")
        db.session.add(author)
        db.session.commit()
        return author


def test_author_create(sample_author, app, db):
    with app.app_context():
        db.session.add(sample_author)
        db.session.commit()
        assert sample_author.name == "Антон Павлович Чехов"


def test_author_update(sample_author):
    sample_author.name = "Антон Михайлович Чехов"
    assert sample_author.name == "Антон Михайлович Чехов"


@pytest.fixture
def sample_book(app, sample_author, db):
    with app.app_context():
        book = Book(title="Идиот")
        book.authors = [sample_author]
        db.session.add(book)
        db.session.commit()
        return book


def test_book_create(sample_book, app, db):
    with app.app_context():
        db.session.add(sample_book)
        db.session.commit()
        assert sample_book.title == "Идиот"
        assert sample_book.authors[0].name == "Антон Павлович Чехов"


def test_book_update(sample_book, app, db):
    with app.app_context():
        db.session.add(sample_book)
        db.session.commit()
        sample_book.title = "Дама с собачкой"
        sample_book.authors[0].name = "Антон Михайлович Чехов"
        assert sample_book.title == "Дама с собачкой"
        assert sample_book.authors[0].name == "Антон Михайлович Чехов"


@pytest.fixture
def sample_user(app, db):
    with app.app_context():
        user = User(username="nais", password_hash="12345678", is_active=False)
        db.session.add(user)
        db.session.commit()
    return user


def test_user_create(sample_user, db, app):
    with app.app_context():
        db.session.add(sample_user)
        db.session.commit()
        assert sample_user.username == "nais"
        assert sample_user.password_hash == "12345678"
        assert sample_user.is_active == False


def test_user_update(sample_user, app, db):
    with app.app_context():
        db.session.add(sample_user)
        db.session.commit()
        sample_user.username = "alkator"
        sample_user.password_hash = "87654321"
        sample_user.is_active = True
        assert sample_user.username == "alkator"
        assert sample_user.password_hash == "87654321"
        assert sample_user.is_active == True