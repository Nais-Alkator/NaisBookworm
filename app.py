from flask import Flask
from dotenv import load_dotenv
import os
from routes import blueprint
from models import db

load_dotenv()


app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(app.root_path, os.environ.get("SQLALCHEMY_DATABASE_URI"))
app.secret_key = os.environ.get("SECRET_KEY")

db.init_app(app)
app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run(debug=True)
