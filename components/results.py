from flask import render_template, redirect, flash, request, url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import abort

from data import db_session
from data.level import Level
from data.result import Result
from data.user import User
from forms.submit_olympiad import SubmitOlympiadForm
from forms.login import LoginForm
from forms.search_user import SearchUserForm
from forms.submit_result import SubmitResultForm

from global_app import get_app
from utils.permissions_required import teacher_required
from utils.utils import get_message_from_form

app = get_app()
current_user: User


@app.route('/results', methods=['GET'])
@teacher_required
def results():
    db_sess = db_session.create_session()
    results = db_sess.query(Result).all()
    return render_template('results.html', **locals())


@app.route('/results/<int:id>', methods=['GET', 'POST'])
@teacher_required
def edit_result(id):
    db_sess = db_session.create_session()
    result = db_sess.query(Result).filter(Result.id == id).first()
    if not result:
        abort(404)

    form = EditOlympiadForm()
    form.name.data = result.name
    levels = {str(i.id): i for i in db_sess.query(Level).all()}
    form.level.choices = [(str(k), v.name) for k, v in levels.items()]
    if form.validate_on_submit():
        olympiad.level_id = levels[form.level.data].id
        olympiad.name = form.name.data
        flash(f'Successfully edited olympiad "{form.name.data}"', category='success')
        db_sess.commit()
        return redirect(url_for('olympiads'))
    else:
        msg = get_message_from_form(form)
        if msg:
            flash(msg, category='danger')

    return render_template('edit_olympiad.html', **locals())


@app.route('/delete_olympiad/<int:id>', methods=['GET'])
@teacher_required
def delete_olympiad(id):
    db_sess = db_session.create_session()
    olympiad = db_sess.query(Olympiad).filter(Olympiad.id == id).first()
    if not olympiad:
        flash('No such olympiad', category='danger')
    else:
        flash(f'Successfully deleted olympiad "{olympiad.name} {olympiad.level.name}"', category='success')
        db_sess.delete(olympiad)
        db_sess.commit()
    return redirect(url_for('olympiads'))


@app.route('/add_result', methods=['GET', 'POST'])
@teacher_required
def add_result():
    db_sess = db_session.create_session()
    form = SubmitResultForm()

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
        return redirect(url_for('olympiads'))
    else:
        msg = get_message_from_form(form)
        if msg:
            flash(msg, category='danger')

    return render_template('add_olympiad.html', **locals())
