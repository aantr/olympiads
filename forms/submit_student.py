from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, \
    IntegerField, FileField, BooleanField, DateField
from wtforms.validators import DataRequired

from data.student import Student


class SubmitStudentForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    middle_name = StringField('Middle name', validators=[])
    birthday = DateField('Birthday', validators=[DataRequired()])
    sex = SelectField('Sex', validators=[DataRequired()], choices=Student.get_sex_choices())
    study = BooleanField('Study')
    n_class = SelectField('Class', validators=[DataRequired()],
                          choices={str(i): i for i in range(1, 12)})

    submit = SubmitField('Add')

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        self.first_name.data = self.first_name.data.strip()
        self.last_name.data = self.last_name.data.strip()
        if self.middle_name.data:
            self.middle_name.data = self.middle_name.data.strip()
        return True
