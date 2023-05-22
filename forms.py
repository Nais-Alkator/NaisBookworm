from wtforms import Form, StringField
from wtforms.validators import DataRequired


class BookForm(Form):
    title = StringField(label="Title", validators=[DataRequired()])


class Author(Form):
    name = StringField(label="Name", validators=[DataRequired()])

