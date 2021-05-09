import os

from flask import render_template, redirect, flash, url_for, send_from_directory
from flask_login import current_user
from werkzeug.exceptions import abort

from data import db_session
from data.file import File
from data.olympiad import Olympiad
from data.result import Result
from data.result_level import ResultLevel
from data.student import Student
from data.user import User
from forms.edit_result import EditResultForm
from forms.submit_result import SubmitResultForm

from global_app import get_app, get_dir
from utils.permissions_required import teacher_required, admin_required
from utils.utils import get_message_from_form

app = get_app()
current_user: User


@app.route('/results', methods=['GET'])
@teacher_required
def results():
    db_sess = db_session.create_session()
    results = db_sess.query(Result).all()
    return render_template('results.html', **locals())


@app.route('/protocol/<int:id>', methods=['GET', 'POST'])
@admin_required
def protocol(id):
    db_sess = db_session.create_session()
    protocol = db_sess.query(File).filter(File.id == id).first()
    if not protocol:
        abort(404)
    base = os.path.join(get_dir(), 'files', 'protocol')
    return send_from_directory(
        directory=base, filename=protocol.get_name(),
        as_attachment=True, attachment_filename='protocol_' + protocol.get_name())


@app.route('/results/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_result(id):
    db_sess = db_session.create_session()
    result = db_sess.query(Result).filter(Result.id == id).first()
    if not result:
        abort(404)
    args = ['date', 'place', 'points', 'location', 'n_class']
    form = EditResultForm(
        olympiad=result.olympiad.id,
        student=result.student.id,
        level=result.level.id if result.level else None,
        **{i: result.__getattribute__(i) for i in args}
    )
    olympiads = {str(i.id): i for i in db_sess.query(Olympiad).order_by(Olympiad.name).all()}
    students = {str(i.id): i for i in db_sess.query(Student).order_by(Student.last_name, Student.first_name).all()}
    levels = {str(i.id): i for i in db_sess.query(ResultLevel).all()}
    form.olympiad.choices = [(str(k), v.get_name()) for k, v in olympiads.items()]
    form.student.choices = [(str(k), v.get_name()) for k, v in students.items()]
    form.level.choices = [('', '')] + [(str(k), v.name) for k, v in levels.items()]

    if form.validate_on_submit():
        result.olympiad_id = olympiads[form.olympiad.data].id
        result.student_id = students[form.student.data].id
        result.date = form.date.data
        result.place = form.place.data
        result.points = form.points.data
        result.level_id = levels[form.level.data].id if form.level.data else None
        result.location = form.location.data
        result.n_class = form.n_class.data

        if form.protocol.data:
            base = os.path.join(get_dir(), 'files', 'protocol')
            if result.protocol:
                os.remove(os.path.join(base, result.protocol.get_name()))
                db_sess.delete(result.protocol)
            protocol = File()
            protocol.extension = os.path.splitext(form.protocol.data.filename)[1][1:]
            db_sess.add(protocol)
            db_sess.flush()
            with open(os.path.join(base, protocol.get_name()), 'wb') as f:
                f.write(form.protocol.data.stream.read())
            result.protocol_id = protocol.id

        flash(f'Successfully edited result', category='success')
        db_sess.commit()
        return redirect(url_for('results'))
    else:
        msg = get_message_from_form(form)
        if msg:
            flash(msg, category='danger')

    return render_template('edit_result.html', **locals())


@app.route('/delete_result/<int:id>', methods=['GET'])
@admin_required
def delete_result(id):
    db_sess = db_session.create_session()
    result = db_sess.query(Result).filter(Result.id == id).first()
    if not result:
        flash('No such result', category='danger')
    else:
        if result.protocol:
            base = os.path.join(get_dir(), 'files', 'protocol')
            os.remove(os.path.join(base, result.protocol.get_name()))
            db_sess.delete(result.protocol)
        flash(f'Successfully deleted result', category='success')
        db_sess.delete(result)
        db_sess.commit()
    return redirect(url_for('results'))


@app.route('/add_result', methods=['GET', 'POST'])
@teacher_required
def add_result():
    db_sess = db_session.create_session()
    form = SubmitResultForm()
    olympiads = {str(i.id): i for i in db_sess.query(Olympiad).order_by(Olympiad.name).all()}
    students = {str(i.id): i for i in db_sess.query(Student).order_by(Student.last_name, Student.first_name).all()}
    levels = {str(i.id): i for i in db_sess.query(ResultLevel).all()}
    form.olympiad.choices = [(str(k), v.get_name()) for k, v in olympiads.items()]
    form.student.choices = [(str(k), v.get_name()) for k, v in students.items()]
    form.level.choices = [('', '')] + [(str(k), v.name) for k, v in levels.items()]

    if form.validate_on_submit():
        result = Result()
        result.olympiad_id = olympiads[form.olympiad.data].id
        result.student_id = students[form.student.data].id
        result.date = form.date.data
        result.points = form.points.data
        result.level_id = levels[form.level.data].id if form.level.data else None
        result.location = form.location.data
        result.n_class = form.n_class.data
        result.place = form.place.data

        if form.protocol.data:
            protocol = File()
            base = os.path.join(get_dir(), 'files', 'protocol')
            protocol.extension = os.path.splitext(form.protocol.data.filename)[1][1:]
            db_sess.add(protocol)
            db_sess.flush()
            with open(os.path.join(base, f'{protocol.id}.{protocol.extension}'), 'wb') as f:
                f.write(form.protocol.data.stream.read())
            result.protocol_id = protocol.id
        db_sess.add(result)
        flash(f'Successfully added result', category='success')
        db_sess.commit()
        if current_user.has_rights_admin():
            return redirect(url_for('results'))
        else:
            return redirect(url_for('add_result'))
    else:
        msg = get_message_from_form(form)
        if msg:
            flash(msg, category='danger')

    return render_template('add_result.html', **locals())
