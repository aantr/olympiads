from flask import Flask, render_template, redirect, url_for, send_from_directory
import os
import socket

from data import db_session
from data.level import Level
from data.result_level import ResultLevel
from data.user import User
import global_app
from utils.init_db import init_db

directory = os.path.dirname(__file__)
SECRET_KEY = 'test_system_secret_key_lkzdt,'
DB = os.path.join(directory, 'db/olympiads.db')

global_app.global_init(__name__, directory)
app = global_app.get_app()
app.config.from_object(__name__)
app.dir = directory
current_user: User

recreate_db = 0


def on_recreate_db():
    print('Recreate db...')
    if os.path.exists(DB):
        os.remove(DB)

    db_session.global_init(app.config['DB'])
    db_sess = db_session.create_session()

    user = User()
    user.username = 'admin'
    user.type = 10
    user.set_password('admin')
    db_sess.add(user)
    user = User()
    user.username = 'teacher'
    user.set_password('teacher')
    db_sess.add(user)

    for i in ['Школьный', 'Муниципальный', 'Региональный', 'Всероссийский']:
        level = Level()
        level.name = i
        db_sess.add(level)
    for i in ['Победитель', 'Призер', 'Участник']:
        level = ResultLevel()
        level.name = i
        db_sess.add(level)

    db_sess.commit()


# Components
import components.login
import components.errors
import components.index
import components.olympiad
import components.result
import components.student
import components.transfer
import components.report


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'img/favicon.ico')


def init():
    if recreate_db:
        on_recreate_db()
    db_session.global_init(app.config['DB'])
    init_db()


def main():
    h_name = socket.gethostname()
    ip_address = socket.gethostbyname(h_name)
    print(ip_address)

    port = int(os.environ.get('PORT', 8080))
    app.run(host='localhost', port=port)


init()
if __name__ == '__main__':
    main()
