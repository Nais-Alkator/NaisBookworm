from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    title = StringField('Название книги', validators=[DataRequired()])
    authors = StringField('Авторы', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class AuthorForm(FlaskForm):
    name = StringField('Имя автора', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
