from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class NewRequestForm(FlaskForm):
    requests = TextAreaField('requests', validators=[DataRequired()])
    submit = SubmitField('Найти LSI слова')
