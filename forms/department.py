from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):

    title = StringField('Название', validators=[DataRequired()])
    members = StringField('Участники')
    email = EmailField('Email')
    submit = SubmitField('Добавить')
