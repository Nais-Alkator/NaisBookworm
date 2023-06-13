import os
import pytest
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from routes import blueprint, login_manager
from flask_migrate import Migrate, init, migrate, upgrade
from flask_sqlalchemy import SQLAlchemy


@pytest.fixture(scope="session")
def db():
    db = SQLAlchemy()
    yield db


@pytest.fixture
def app(db):
    app = Flask(__name__, template_folder="../templates")
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + "../instance/test_db2.db"
    app.config['TESTING'] = True
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
    app.config['SECRET_KEY'] = 'secret_key'
    login_manager.init_app(app)
    app.debug = True
    app.register_blueprint(blueprint)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print(db.Query)
        print(db.metadatas)
        print(db.Model)
        yield app
        db.create_all()
