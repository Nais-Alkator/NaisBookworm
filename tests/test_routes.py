from models import Author, Book
from flask_login import login_user


def test_get_registration_form(client):
    response = client.get('/registration')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data


def test_get_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data
    assert b'class="login-form' in response.data


def test_get_authors(client):
    response = client.get('/authors')
    decoded_html = response.data.decode("utf-8")
    assert response.status_code == 200
    assert '<!DOCTYPE html>' in decoded_html
    assert '<h1>Список авторов</h1>' in decoded_html


def test_get_books(client):
    response = client.get('/books')
    decoded_html = response.data.decode("utf-8")
    assert response.status_code == 200
    assert '<!DOCTYPE html>' in decoded_html
    assert '<h1>Список книг</h1>' in decoded_html


def test_add_author(client, app, authenticated_user):
    with app.test_request_context():
        form_data = {
            'name': 'John Smith',
        }
        login_user(authenticated_user)
        response = client.post('/add_author', data=form_data, follow_redirects=True)
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
        author = Author.query.filter_by(name='John Smith').first()
        assert author is not None


def test_list_author_books(client):
    author = Author.query.first()
    response = client.get(f'/author_books/{author.id}')
    decoded_html = response.data.decode("utf-8")
    assert response.status_code == 200
    assert '<!DOCTYPE html>' in decoded_html
    assert f'<title>NaisBookworm - {author.name}</title>' in decoded_html


def test_delete_author(client, authenticated_user):
    author = Author.query.first()
    login_user(authenticated_user)
    response = client.delete(f'/delete_author/{author.id}/', follow_redirects=True)
    decoded_html = response.data.decode("utf-8")
    deleted_author = Author.query.first()
    assert response.status_code == 200
    assert '<!DOCTYPE html>' in decoded_html
    assert f"Автор {author.name} успешно удален" in decoded_html
    assert deleted_author is None


def test_update_author(client, authenticated_user, database):
    author = Author(name="Conan Doyle")
    database.session.add(author)
    database.session.commit()
    login_user(authenticated_user)
    form_data = {"name": "Arthur Conan Doyle"}
    response = client.put(f"/update_author/{author.id}", data=form_data, follow_redirects=True)
    updated_author = Author.query.filter_by(name="Arthur Conan Doyle").first()
    decoded_html = response.data.decode("utf-8")
    assert response.status_code == 200
    assert updated_author.name == "Arthur Conan Doyle"
    assert f"Автор успешно изменен." in decoded_html


def test_add_book(client, app, authenticated_user):
    with app.test_request_context():
        form_data = {
            "title": "Шерлок Холмс",
            "authors-0": "Артур Конан Дойл",
        }
        # Flask не предусматривает передачу значений в виде списка для аргумента data post запроса
        login_user(authenticated_user)
        response = client.post('/add_book', data=form_data, follow_redirects=True)
        decoded_html = response.data.decode("utf-8")
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
        assert 'Книга успешно добавлена.' in decoded_html
        book = Book.query.filter_by(title="Шерлок Холмс").first()
        assert book.title == "Шерлок Холмс"
        assert book.authors[0].name == "Артур Конан Дойл"


def test_get_book(client):
    book = Book.query.first()
    response = client.get(f'/book/{book.id}')
    decoded_html = response.data.decode('utf-8')
    assert response.status_code == 200
    assert f"<h1>{book.title}</h1>" in decoded_html


def test_delete_book(client, authenticated_user):
    book = Book.query.first()
    login_user(authenticated_user)
    response = client.delete(f'/delete_book/{book.id}/', follow_redirects=True)
    decoded_html = response.data.decode("utf-8")
    deleted_book = Book.query.filter_by(title=book.title).first()
    assert response.status_code == 200
    assert '<!DOCTYPE html>' in decoded_html
    assert f"Книга {book.title} успешно удалена" in decoded_html
    assert deleted_book is None