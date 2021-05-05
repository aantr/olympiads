from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from forms.utils.multiply_checkbox_field import MultiplyCheckboxField


class AddOlympiadForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    levels = MultiplyCheckboxField('level_checkbox', 'Levels')
    submit = SubmitField('Add')

    def validate(self):
        self.levels.checked = []
        for i in self.levels.choices:
            if self.levels.prefix_id + i[0] in request.form:
                self.levels.checked.append(i[0])
        if not FlaskForm.validate(self):
            return False
        if not self.levels.checked:
            self.levels.errors.append('At least one level should be selected')
            return False
        return True
