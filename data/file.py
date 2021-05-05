import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class File(SqlAlchemyBase):
    __tablename__ = 'file'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    extension = sqlalchemy.Column(sqlalchemy.String)
