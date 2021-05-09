from flask import render_template, redirect, flash, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import func
from werkzeug.exceptions import abort

from data import db_session
from data.level import Level
from data.olympiad import Olympiad
from data.user import User
from forms.edit_olympiad import EditOlympiadForm
from forms.submit_olympiad import SubmitOlympiadForm

from global_app import get_app
from utils.permissions_required import teacher_required, admin_required
from utils.utils import get_message_from_form

app = get_app()
current_user: User


@app.route('/olympiads', methods=['GET'])
@admin_required
def olympiads():
    db_sess = db_session.create_session()
    olympiads = db_sess.query(Olympiad).order_by(Olympiad.name).all()
    return render_template('olympiads.html', **locals())


@app.route('/olympiads/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_olympiad(id):
    db_sess = db_session.create_session()
    olympiad = db_sess.query(Olympiad).filter(Olympiad.id == id).first()
    if not olympiad:
        abort(404)
    args = ['name']
    form = EditOlympiadForm(
        level=str(olympiad.level.id),
        **{i: olympiad.__getattribute__(i) for i in args}
    )
    levels = {str(i.id): i for i in db_sess.query(Level).all()}
    form.level.choices = [(str(k), v.name) for k, v in levels.items()]

    if form.validate_on_submit():
        olympiad_ = db_sess.query(Olympiad).filter(func.lower(Olympiad.name) == func.lower(form.name.data)). \
            filter(Olympiad.level_id == levels[form.level.data].id).\
            filter(Olympiad.id != olympiad.id).first()
        if olympiad_:
            flash('Olympiad with such name already exists', category='danger')
            return render_template('edit_olympiad.html', **locals())

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
@admin_required
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


@app.route('/add_olympiad', methods=['GET', 'POST'])
@admin_required
def add_olympiad():
    db_sess = db_session.create_session()
    form = SubmitOlympiadForm()
    levels = {str(i.id): i for i in db_sess.query(Level).all()}
    form.levels.choices = [(str(k), v.name) for k, v in levels.items()]
    if form.validate_on_submit():
        level_ids = [levels[i].id for i in form.levels.checked]
        olympiad = db_sess.query(Olympiad).filter(func.lower(Olympiad.name) == func.lower(form.name.data)).\
            filter(Olympiad.level_id.in_(level_ids)).first()
        if olympiad:
            flash('Olympiad with such name already exists', category='danger')
            return render_template('add_olympiad.html', **locals())

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
