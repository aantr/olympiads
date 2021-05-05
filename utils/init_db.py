from data import db_session


def init_db():
    db_sess = db_session.create_session()
