import pytest
from models import Author, Book, User
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from routes import blueprint, login_manager


@pytest.fixture
def sample_app(sample_db):
    app = Flask(__name__, template_folder="templates")
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + "../instance/library.db"
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
    app.secret_key = os.environ.get("SECRET_KEY")
    sample_db.init_app(app)
    login_manager.init_app(app)
    app.debug = True
    app.register_blueprint(blueprint)

    with app.app_context():
        sample_db.create_all()
        yield app
        sample_db.drop_all()


@pytest.fixture
def sample_db():
    db = SQLAlchemy()
    return db


@pytest.fixture
def sample_author(sample_app):
    with sample_app.app_context():
        author = Author(name="Антон Павлович Чехов")
        return author


def test_author_create(sample_author, sample_app):
    with sample_app.app_context():
        assert sample_author.name == "Антон Павлович Чехов"


def test_author_update(sample_author):
    sample_author.name = "Антон Михайлович Чехов"
    assert sample_author.name == "Антон Михайлович Чехов"


@pytest.fixture
def sample_book(sample_app, sample_author):
    with sample_app.app_context():
        book = Book(title="Идиот")
        book.authors = [sample_author]
        return book


def test_book_create(sample_book):
    assert sample_book.title == "Идиот"
    assert sample_book.authors[0].name == "Антон Павлович Чехов"


def test_book_update(sample_book):
    sample_book.title = "Дама с собачкой"
    sample_book.authors[0].name = "Антон Михайлович Чехов"
    assert sample_book.title == "Дама с собачкой"
    assert sample_book.authors[0].name == "Антон Михайлович Чехов"


@pytest.fixture
def sample_user(sample_app):
    with sample_app.app_context():
        user = User(username="nais", password_hash="12345678", is_active=False)
    return user


def test_user_create(sample_user):
    assert sample_user.username == "nais"
    assert sample_user.password_hash == "12345678"
    assert sample_user.is_active == False


def test_user_update(sample_user):
    sample_user.username = "alkator"
    sample_user.password_hash = "87654321"
    sample_user.is_active = True
    assert sample_user.username == "alkator"
    assert sample_user.password_hash == "87654321"
    assert sample_user.is_active == True