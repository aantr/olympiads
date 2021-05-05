import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class Olympiad(SqlAlchemyBase):
    __tablename__ = 'olympiad'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    level_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('level.id'))
    level = sqlalchemy.orm.relation('Level')