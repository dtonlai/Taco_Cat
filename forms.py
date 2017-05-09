from flask_wtf import Form
from wtforms import StringField, PasswordField, RadioField
from wtforms.validators import DataRequired, Regexp, Email, Length, ValidationError, EqualTo

from models import User

def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError("Sorry, that name is already taken!")

def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("Sorry, that e-mail is already in use!")

class RegisterForm(Form):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, "
                         "numbers, and underscores only.")
            ),
            name_exists
        ]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            email_exists,
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo("password2", message="The passwords don't match!")
        ]
    )
    password2 = PasswordField(
        "Verify Password",
        validators=[DataRequired()]
    )

class LoginForm(Form):
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

class TacoForm(Form):
    protein = StringField(
        "Protein",
        validators=[DataRequired()]
    )
    shell = StringField(
        "Shell",
        validators=[DataRequired()]
    )
    extras = StringField(
        "Extras",
        validators=[DataRequired()]
    )
    cheese = RadioField(
        "Cheese?",
        choices=[("Yes", "Yes"), ("No", "No")], default="Yes"
    )


