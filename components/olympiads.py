from flask import render_template, redirect, flash, request, url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import abort

from data import db_session
from data.level import Level
from data.olympiad import Olympiad
from data.user import User
from forms.add_olympiad import AddOlympiadForm
from forms.login import LoginForm
from forms.search_user import SearchUserForm

from global_app import get_app
from utils.permissions_required import teacher_required
from utils.utils import get_message_from_form

app = get_app()
current_user: User


@app.route('/olympiads', methods=['GET'])
@teacher_required
def olympiads():
    db_sess = db_session.create_session()
    olympiads = db_sess.query(Olympiad).all()
    return render_template('olympiads.html', **locals())


@app.route('/add_olympiad', methods=['GET', 'POST'])
@teacher_required
def add_olympiad():
    db_sess = db_session.create_session()
    form = AddOlympiadForm()
    levels = {str(i.id): i for i in db_sess.query(Level).all()}
    form.levels.choices = [(str(k), v.name) for k, v in levels.items()]
    if form.validate_on_submit():
        for i in form.levels.checked:
            level: Level = levels[i]
            olympiad = Olympiad()
            olympiad.level_id = level.id
            olympiad.name = form.name.data
            db_sess.add(olympiad)
            db_sess.flush()

        flash(f'Successfully added olympiad "{form.name.data}"', category='success')
        db_sess.commit()
        return redirect(url_for('add_olympiad'))
    else:
        msg = get_message_from_form(form)
        if msg:
            flash(msg, category='danger')

    return render_template('add_olympiad.html', **locals())
