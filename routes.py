from flask import Blueprint, render_template, request, redirect, flash, url_for
from models import Author, Book, User, db
from forms import AuthorForm, BookForm, RegistrationForm, LoginForm
from flask_login import current_user, login_user
from flask_login import LoginManager


blueprint = Blueprint("routes", __name__)
login_manager = LoginManager()


@blueprint.route('/')
def get_home():
    login_form = LoginForm()
    return render_template("index.html", form=login_form)


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
    flash(f"Автор {author.name} успешно удален")
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


@blueprint.route("/book/<int:book_id>")
def get_book(book_id):
    book = Book.query.get(book_id)
    authors = list(book.authors)
    form = BookForm()
    return render_template("book.html", book=book, authors=authors, form=form)


@blueprint.route("/delete_book/<int:book_id>/", methods=["DELETE", "GET"])
def delete_book(book_id):
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    flash(f"Книга {book.title} успешно удалена")
    return redirect(url_for("routes.get_books"))


@blueprint.route("/update_book/<int:book_id>", methods=["GET", "POST"])
def update_book(book_id):
    if request.method == 'PUT' or request.form.get('_method') == 'PUT':
        form = BookForm(request.form)
        if form.validate():
            book = Book.query.get(book_id)
            book.title = form.title.data
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
            book.authors = authors
            db.session.commit()
            flash('Книга успешно изменена.')
            return redirect(url_for('routes.get_books'))
        else:
            flash('Ошибка валидации формы.')
            return redirect(url_for('routes.get_books'))


@blueprint.route("/search_book")
def search_book():
    query = request.args.get('query')  
    book = Book.query.filter(Book.title.ilike(f"{query}")).first()
    if book:
        return redirect(url_for('routes.get_book', book_id=book.id))
    else:
        flash('Книга не найдена.')
        return redirect(url_for('routes.get_books'))


@blueprint.route("/registration")
def get_registration_form():
    form = RegistrationForm()
    return render_template("registration.html", form=form)


@blueprint.route("/registration", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались! Теперь вы можете войти в систему.')
        return redirect(url_for('routes.get_home'))
    return render_template('registration.html', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
@login_manager.user_loader
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.get_home'))
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильное имя пользователя или пароль')
            return redirect(url_for('routes.login'))

        login_user(user, remember=form.remember_me.data)
        flash("Вы успешно авторизовались")
        return redirect(url_for('routes.get_home'))
    print(form.validate_on_submit())
    print(form.errors)
    return render_template("index.html", form=form)