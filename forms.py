from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    authors = FieldList(StringField('Автор'), min_entries=1)
    submit = SubmitField('Сохранить')


class AuthorForm(FlaskForm):
    name = StringField('Имя автора', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
