import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Result(SqlAlchemyBase):
    __tablename__ = 'result'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    olympiad_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('olympiad.id'))
    olympiad = sqlalchemy.orm.relation('Olympiad')
    student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('student.id'))
    student = sqlalchemy.orm.relation('Student')
    date = sqlalchemy.Column(sqlalchemy.Date)
    place = sqlalchemy.Column(sqlalchemy.Integer)
    points = sqlalchemy.Column(sqlalchemy.Integer)
    location = sqlalchemy.Column(sqlalchemy.String)
    protocol_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('file.id'))
    protocol = sqlalchemy.orm.relation('File')
    n_class = sqlalchemy.Column(sqlalchemy.Integer)
