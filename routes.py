from flask import Blueprint, render_template, request, redirect, flash, url_for
from models import Author, Book, db
from forms import AuthorForm, BookForm


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
    form = BookForm()
    return render_template("books.html", books=books, form=form)


@blueprint.route("/add_author", methods=["POST"])
def add_author():
    form = AuthorForm(request.form)
    if form.validate():
        new_author = Author(name=form.name.data)
        db.session.add(new_author)
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
    form = AuthorForm()
    return render_template("author_books.html", author_books=author_books, author=author, form=form)


@blueprint.route("/delete_author/<int:author_id>/", methods=["DELETE", "GET"])
def delete_author(author_id):
    author = Author.query.get(author_id)
    db.session.delete(author)
    db.session.commit()
    flash(f"Авто {author.name} успешно удален")
    return redirect(url_for("routes.get_authors"))


@blueprint.route("/update_author/<int:author_id>", methods=["PUT", "GET", "POST"])
def update_author(author_id):
    if request.method == 'PUT' or request.form.get('_method') == 'PUT':
        form = AuthorForm(request.form)
        if form.validate():
            author = Author.query.get(author_id)
            author.name = form.name.data
            db.session.commit()
            flash('Автор успешно изменен.')
            return redirect(url_for('routes.get_authors'))
        else:
            print(form.errors)
            flash('Ошибка валидации формы.')
            return redirect(url_for('routes.get_authors'))


@blueprint.route("/add_book", methods=["POST"])
def add_book():
    form = BookForm(request.form)
    if form.validate():
        author_names = form.authors.data
        authors = []

        for author_name in author_names:
            author = Author.query.filter_by(name=author_name).first()

            if author:
                authors.append(author)
            else:
                new_author = Author(name=author_name)
                db.session.add(new_author) 
                authors.append(new_author)

        new_book = Book(title=form.title.data)
        new_book.authors = authors  

        db.session.add(new_book)
        db.session.commit()
        flash('Книга успешно добавлена.')
        return redirect(url_for('routes.get_books'))
    else:
        flash('Ошибка валидации формы.')
        return redirect(url_for('routes.get_books'))
