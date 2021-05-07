import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from utils.utils import date_format
from .db_session import SqlAlchemyBase


class Student(SqlAlchemyBase):
    __tablename__ = 'student'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    first_name = sqlalchemy.Column(sqlalchemy.String)
    last_name = sqlalchemy.Column(sqlalchemy.String)
    middle_name = sqlalchemy.Column(sqlalchemy.String)
    birthday = sqlalchemy.Column(sqlalchemy.Date)
    sex = sqlalchemy.Column(sqlalchemy.Integer)
    study = sqlalchemy.Column(sqlalchemy.Boolean)
    n_class = sqlalchemy.Column(sqlalchemy.Integer)

    def get_name(self):
        return f'{self.last_name} {self.first_name}' + (f' {self.middle_name}' if self.middle_name else '')

    def get_birthday(self):
        return self.birthday.strftime(date_format())

    def get_study(self):
        return 'Yes' if self.study else 'No'

    @staticmethod
    def get_sex_choices():
        return ['Male', 'Female']

    def get_sex(self):
        return self.get_sex_choices()[int(self.sex)]
