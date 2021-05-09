from flask import request
from flask_wtf import FlaskForm
from wtforms import validators, StringField, SubmitField, SelectField, DateField, IntegerField, FileField
from wtforms.validators import DataRequired, NumberRange


class EditResultForm(FlaskForm):
    olympiad = SelectField('Olympiad', validators=[DataRequired()])
    student = SelectField('Student', validators=[DataRequired()])

    date = DateField('Date', validators=[DataRequired()])
    place = IntegerField('Place', validators=[
        NumberRange(min=1, message='Слишком маленькое число'), validators.optional()])
    points = IntegerField('Points', validators=[
        NumberRange(min=0, message='Слишком маленькое число'), validators.optional()])
    level = SelectField('Level', validators=[])
    location = StringField('Location', validators=[])
    protocol = FileField('Protocol', validators=[])
    n_class = SelectField('Class', validators=[DataRequired()],
                          choices={str(i): i for i in range(1, 12)})
    submit = SubmitField('Save')

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.protocol.data and '.' not in self.protocol.data.filename:
            self.protocol.errors.append('Invalid filename')
            return False
        self.level.data = self.level.data.strip()
        self.location.data = self.location.data.strip()
        return True
