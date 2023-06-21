from models import Author
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