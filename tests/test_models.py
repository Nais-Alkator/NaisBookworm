import pytest
from models import Author, Book, User




@pytest.fixture
def sample_author(app, db):
    author = Author(name="Фёдор Михайлович Достоевский")
    return author


def test_author_create(sample_author, app, db):
    assert sample_author.name == "Фёдор Михайлович Достоевский"
        

def test_author_update(sample_author):
    sample_author.name = "Антон Михайлович Чехов"
    assert sample_author.name == "Антон Михайлович Чехов"


@pytest.fixture
def sample_book(sample_author):
    book = Book(title="Идиот")
    book.authors = [sample_author]
    return book
        


def test_book_create(sample_book):
        assert sample_book.title == "Идиот"
        assert sample_book.authors[0].name == "Фёдор Михайлович Достоевский"
        

def test_book_update(sample_book):
    sample_book.title = "Дама с собачкой"
    sample_book.authors[0].name = "Антон Михайлович Чехов"
    assert sample_book.title == "Дама с собачкой"
    assert sample_book.authors[0].name == "Антон Михайлович Чехов"
        

@pytest.fixture
def sample_user():
    user = User(username="asdfgh12345", password_hash="1234567891", is_active=False)
    return user


def test_user_create(sample_user, db, app):
    assert sample_user.username == "asdfgh12345"
    assert sample_user.password_hash == "1234567891"
    assert sample_user.is_active == False


def test_user_update(sample_user):
    sample_user.username = "alkator1"
    sample_user.password_hash = "87654321"
    sample_user.is_active = True
    assert sample_user.username == "alkator1"
    assert sample_user.password_hash == "87654321"
    assert sample_user.is_active == True
        