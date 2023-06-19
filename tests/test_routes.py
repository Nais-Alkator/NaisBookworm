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
