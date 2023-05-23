from flask import Flask
from routes import blueprint
from dotenv import load_dotenv
import os
load_dotenv()


app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.register_blueprint(blueprint)
app.secret_key = os.environ.get("SECRET_KEY")


if __name__ == '__main__':
    app.run(debug=True)