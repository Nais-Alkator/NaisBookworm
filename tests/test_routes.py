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
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
