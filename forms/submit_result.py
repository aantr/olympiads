from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FileField, DateField
from wtforms.validators import DataRequired


class SubmitResultForm(FlaskForm):
    olympiad = SelectField('Olympiad', validators=[DataRequired()])
    student = SelectField('Student', validators=[DataRequired()])

    date = DateField('Date', validators=[DataRequired()])
    place = IntegerField('Place', validators=[DataRequired()])
    points = IntegerField('Points', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    protocol = FileField('Protocol', validators=[])
    n_class = SelectField('Class', validators=[DataRequired()],
                          choices={str(i): i for i in range(1, 12)})
    submit = SubmitField('Add')

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.protocol.data and '.' not in self.protocol.data.filename:
            self.protocol.errors.append('Invalid filename')
            return False
        self.location.data = self.location.data.strip()
        return True