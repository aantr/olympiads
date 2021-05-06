from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, IntegerField, FileField
from wtforms.validators import DataRequired


class SubmitResultForm(FlaskForm):
    olympiad = SelectField('Olympiad', validators=[DataRequired()])
    student = SelectField('Student', validators=[DataRequired()])
    student = SelectField('Student', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    place = IntegerField('Place', validators=[DataRequired()])
    points = IntegerField('Date', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    protocol = FileField('Protocol', validators=[DataRequired()])
    n_class = IntegerField('Class', validators=[DataRequired()])

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        return True
