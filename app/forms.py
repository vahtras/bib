from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SearchForm(FlaskForm):
    title = StringField('Titel', validators=[])
    author = StringField('Författare', validators=[])
    series = StringField('Serie', validators=[])
    submit = SubmitField()
