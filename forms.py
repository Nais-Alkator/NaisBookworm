from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo


class BookForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    authors = FieldList(StringField('Автор'), min_entries=1)
    submit = SubmitField('Сохранить')


class AuthorForm(FlaskForm):
    name = StringField('Имя автора', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')