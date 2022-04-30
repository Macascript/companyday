from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    email = StringField('Introduzca su Email', validators=[InputRequired()])
    password = PasswordField('Contraseña', validators=[InputRequired()])