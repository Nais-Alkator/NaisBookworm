from flask import Flask
from dotenv import load_dotenv
import os
from routes import blueprint
from models import db
from flask_debugtoolbar import DebugToolbarExtension

load_dotenv()


app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(app.root_path, os.environ.get("SQLALCHEMY_DATABASE_URI"))
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config['FLASH_MESSAGES_OPTIONS'] = {'duration': 5000}
app.secret_key = os.environ.get("SECRET_KEY")
db.init_app(app)
app.debug = True
toolbar = DebugToolbarExtension(app)
app.register_blueprint(blueprint)


if __name__ == '__main__':
    app.run()
