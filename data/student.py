import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

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