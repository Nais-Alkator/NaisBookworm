from models import Author, Book, User
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


def test_search_book(client, app, authenticated_user):
    with app.test_request_context():
        
        query = "query=Шерлок+Холмс"
        response = client.get(f"/search_book?{query}", follow_redirects=True)
        decoded_html = response.data.decode('utf-8')
        assert response.status_code == 200
        assert "<h1>Шерлок Холмс</h1>" in decoded_html


def test_update_book(client, app, authenticated_user):
    with app.test_request_context():
        book = Book.query.filter_by(title="Шерлок Холмс").first()
        form_data = {
            "title": "Шерлок Холмс приключения",
            "authors-0": "Конан Дойл",
        }
        login_user(authenticated_user)
        response = client.put(f'/update_book/{book.id}', data=form_data, follow_redirects=True)
        decoded_html = response.data.decode("utf-8")
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
        assert 'Книга успешно изменена.' in decoded_html
        book = Book.query.filter_by(title="Шерлок Холмс приключения").first()
        assert book.title == "Шерлок Холмс приключения"
        assert book.authors[0].name == "Конан Дойл"


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


def test_get_registration_form(client):
    response = client.get('/registration')
    decoded_html = response.data.decode('utf-8')
    assert response.status_code == 200
    assert "<title>NaisBookworm - Регистрация пользователя</title>" in decoded_html


def test_register(client, app):
    with app.test_request_context():
        form = {"username": "nais", "password": "12345678", "confirm_password": "12345678"}
        response = client.post('/registration', data=form, follow_redirects=True)
        decoded_html = response.data.decode('utf-8')
        user = User.query.filter_by(username="nais").first()
        assert response.status_code == 200
        assert 'Вы успешно зарегистрировались! Теперь вы можете войти в систему.' in decoded_html
        assert user.username == "nais"


def test_login(client, app):
    with app.test_request_context():
        form = {"username": "nais", "password": "12345678", "remember_me": True}
        response = client.post('/login', data=form, follow_redirects=True)
        decoded_html = response.data.decode('utf-8')
        assert response.status_code == 200
        assert f"Вы успешно авторизовались как nais" in decoded_html


def test_logout(client, app):
    with app.test_request_context():
        login_form = {"username": "nais", "password": "12345678", "remember_me": True}
        login = client.post('/login', data=login_form, follow_redirects=True)
        logout= client.get('/logout', follow_redirects=True)
        decoded_html = logout.data.decode('utf-8')
        assert logout.status_code == 200
        assert 'Вы успешно вышли из учетной записи.' in decoded_html