import pytest
from flask import Flask
from routes import blueprint, login_manager, login_user, logout_user
from models import db, User


@pytest.fixture(scope='session')
def app(database):
    app = Flask(__name__, template_folder="../templates")
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + "../instance/test_db.db"
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
    app.config["TESTING"] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.secret_key = "12345"
    login_manager.init_app(app)
    app.debug = True
    app.register_blueprint(blueprint)
    database.init_app(app)

    with app.app_context():
        database.create_all()
        yield app
        database.drop_all()
        

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def database():
    return db


@pytest.fixture(scope='function')
def authenticated_user(app):
    user = User(username='john', password_hash='password', is_active=True)
    with app.test_request_context():
        login_user(user)
        yield user
        logout_user()