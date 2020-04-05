import flask_wtf
import wtforms
from wtforms import validators


class AddForm(flask_wtf.FlaskForm):
    number = wtforms.IntegerField(
        "Question number", validators=[validators.DataRequired()])
    question = wtforms.TextAreaField(
        "Question", validators=[validators.DataRequired()])
    answer = wtforms.TextAreaField(
        "Answer", validators=[validators.DataRequired()])
    submit = wtforms.SubmitField("Submit")
