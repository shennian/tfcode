from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(Form):
    name = SubmitField("what is your name?", validators=[DataRequired()])
    submit = SubmitField("submit")
