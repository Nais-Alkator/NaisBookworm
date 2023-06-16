import pytest
from flask import Flask
from routes import blueprint, login_manager
from models import db


@pytest.fixture(scope='function')
def app():
    app = Flask(__name__, template_folder="../templates")
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + "../instance/test_db.db"
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
    app.config["TESTING"] = True
    app.secret_key = "alkator"
    login_manager.init_app(app)
    app.debug = True
    app.register_blueprint(blueprint)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()
