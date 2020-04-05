import flask_wtf
import wtforms
from wtforms import validators


class LoginForm(flask_wtf.FlaskForm):
    password = wtforms.PasswordField(
        "Password", validators=[validators.DataRequired()])
    submit = wtforms.SubmitField("Submit")
