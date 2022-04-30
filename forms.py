from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    email = EmailField('Introduzca su Email', validators=[InputRequired()])
    password = PasswordField('Contraseña', validators=[InputRequired()])