from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FileField, DateField
from wtforms.validators import DataRequired


class ReportForm(FlaskForm):
    last_name = StringField('Last name')
    n_class = SelectField('Class', choices={str(i): i for i in [''] + list(range(1, 12))})
    olympiad = SelectField('Olympiad')
    level = SelectField('Level')
    apply = SubmitField('Apply')
    get_report = SubmitField('Get report')

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        self.last_name.data = self.last_name.data.strip()
        self.olympiad.data = self.olympiad.data.strip()
        return True
