from flask import Blueprint, render_template
from models import Author


blueprint = Blueprint("routes", __name__)

@blueprint.route('/')
def get_home():
    return render_template("index.html")

@blueprint.route('/authors')
def get_authors():
    authors = Author.query.all()
    return render_template("authors.html", authors=authors)
