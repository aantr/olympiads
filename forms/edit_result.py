from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class EditOlympiadForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    level = SelectField('Level', validators=[DataRequired()])
    submit = SubmitField('Save')

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        return True
