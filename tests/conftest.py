import pytest
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from routes import blueprint, login_manager


@pytest.fixture
def db():
    db = SQLAlchemy()
    return db

    
@pytest.fixture
def app(db):
    app = Flask(__name__, template_folder="templates")
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + "../instance/test_db.db"
    app.config['TESTING'] = True
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
    app.secret_key = os.environ.get("SECRET_KEY")
    db.init_app(app)
    login_manager.init_app(app)
    app.debug = True
    app.register_blueprint(blueprint)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


