from flask_wtf import FlaskForm
import wtforms as wf

from . import app
from .models import Position


def get_position():
    with app.app_context():
        positions = Position.query.all()
        choices = []
        for position in positions:
            choices.append((position.id, position.name))
        return choices


class PositionForm(FlaskForm):
    name = wf.StringField(label='Название должности', validators=[
        wf.validators.DataRequired()
    ])
    department = wf.StringField(label='Отдел')
    wage = wf.IntegerField(label='Ставка заработной платы', validators=[
        wf.validators.DataRequired(),
        wf.validators.NumberRange(min=0)
    ])


class EmployeeForm(FlaskForm):
    name = wf.StringField(label='ФИО клиента', validators=[
        wf.validators.DataRequired()
    ])
    inn = wf.StringField(label='ИНН', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(min=14, max=14)
    ])
    position_id = wf.SelectField(label='Должность', choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.position_id.choices = get_position()

    def validate_inn(self, field):
        if not field.data.startswith('1') and not field.data.startswith('2'):
            raise wf.ValidationError('ИНН должен начинаться с 1 или 2')


class UserForm(FlaskForm):
    username = wf.StringField(label='Логин пользователя', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(min=8, max=24)
    ])
    password = wf.PasswordField(label='Пароль', validators=[
        wf.validators.DataRequired()
    ])

    def validate_password(self, field):
        if field.data.isdigit() or field.data.isalpha():
            raise wf.ValidationError('Пароль должен содержать числа и буквы')
