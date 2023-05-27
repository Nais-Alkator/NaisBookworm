from flask import Blueprint, render_template, request, redirect, flash, url_for
from models import Author, Book, db
from forms import AuthorForm
from time import sleep
blueprint = Blueprint("routes", __name__)

@blueprint.route('/')
def get_home():
    return render_template("index.html")

@blueprint.route('/authors', methods=["GET", "POST"])
def get_authors():
    form = AuthorForm()
    authors = Author.query.all()
    return render_template("authors.html", authors=authors, form=form)

@blueprint.route('/books')
def get_books():
    books = Book.query.all()
    return render_template("books.html", books=books)

@blueprint.route("/add_author", methods=["POST"])
def add_author():
    form = AuthorForm(request.form)
    if form.validate():
        author = Author(name=form.name.data)
        db.session.add(author)
        db.session.commit()
        flash('Автор успешно добавлен.')
        return redirect(url_for('routes.get_authors'))
    else:
        flash('Ошибка валидации формы.')
        return redirect(url_for('routes.get_authors'))

@blueprint.route("/author_books/<int:author_id>")
def list_author_books(author_id):
    author = Author.query.get(author_id)
    author_books = list(author.books)
    return render_template("author_books.html", author_books=author_books, author_name=author.name)