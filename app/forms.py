from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, TimeField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя уже занято.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email уже зарегистрирован.')

class AppointmentForm(FlaskForm):
    master = SelectField('Мастер', coerce=int, validators=[DataRequired()])
    service = SelectField('Услуга', coerce=int, validators=[DataRequired()])
    date = DateField('Дата', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Время', format='%H:%M', validators=[DataRequired()])
    submit = SubmitField('Записаться')

class RoleForm(FlaskForm):
    name = StringField('Название роли', validators=[DataRequired(), Length(max=50)])
    description = StringField('Описание', validators=[Length(max=200)])
    permissions = SelectMultipleField('Права', coerce=int)
    submit = SubmitField('Сохранить')

class UserEditForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    active = BooleanField('Активен')
    roles = SelectMultipleField('Роли', coerce=int)
    submit = SubmitField('Сохранить')