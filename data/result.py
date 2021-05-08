import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import backref

from utils.utils import date_format
from .db_session import SqlAlchemyBase


class Result(SqlAlchemyBase):
    __tablename__ = 'result'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    olympiad_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey('olympiad.id'), nullable=False)
    olympiad = sqlalchemy.orm.relation('Olympiad',
                                       backref=backref('result', cascade='all,delete'))
    student_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey('student.id'), nullable=False)
    student = sqlalchemy.orm.relation('Student',
                                      backref=backref('result', cascade='all,delete'))
    date = sqlalchemy.Column(sqlalchemy.Date)
    place = sqlalchemy.Column(sqlalchemy.Integer)
    points = sqlalchemy.Column(sqlalchemy.Integer)
    level = sqlalchemy.Column(sqlalchemy.String)
    location = sqlalchemy.Column(sqlalchemy.String)
    protocol_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey('file.id'))
    protocol = sqlalchemy.orm.relation('File')
    n_class = sqlalchemy.Column(sqlalchemy.Integer)

    def get_date(self):
        return self.date.strftime(date_format())
