from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms import DateTimeLocalField, DateField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = StringField('Опсание', validators=[DataRequired()])
    work_size = IntegerField('Время работы')
    collaborators = StringField('Участники')
    start_date = DateField('Дата начала', format="%Y-%m-%d")
    end_date = DateField('Дата конца', format="%Y-%m-%d")
    is_finished = BooleanField("Закончена")
    submit = SubmitField('Добавить')
