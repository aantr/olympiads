from flask import render_template, redirect, flash, url_for
from sqlalchemy import func
from werkzeug.exceptions import abort

from data import db_session
from data.student import Student
from data.user import User
from forms.edit_student import EditStudentForm
from forms.submit_student import SubmitStudentForm

from global_app import get_app
from utils.permissions_required import teacher_required, admin_required
from utils.utils import get_message_from_form

app = get_app()
current_user: User


@app.route('/students', methods=['GET'])
@admin_required
def students():
    db_sess = db_session.create_session()
    students = db_sess.query(Student).order_by(Student.last_name, Student.first_name).all()
    return render_template('students.html', **locals())


@app.route('/students/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_student(id):
    db_sess = db_session.create_session()
    student = db_sess.query(Student).filter(Student.id == id).first()
    if not student:
        abort(404)

    args = ['birthday', 'first_name', 'last_name', 'middle_name', 'study']
    form = EditStudentForm(
        sex=student.get_sex(),
        n_class=str(student.n_class),
        **{i: student.__getattribute__(i) for i in args}
    )
    if form.validate_on_submit():
        student_ = db_sess.query(Student).filter(func.lower(Student.last_name) == func.lower(form.last_name.data)). \
            filter(func.lower(Student.first_name) == func.lower(form.first_name.data)).first()
        if student_:
            flash('Student with such last name and first name already exists', category='danger')
            return render_template('edit_student.html', **locals())
        student.sex = Student.get_sex_choices().index(form.sex.data)
        student.study = form.study.data
        student.birthday = form.birthday.data
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.middle_name = form.middle_name.data
        student.n_class = form.n_class.data

        db_sess.commit()
        flash(f'Successfully edited student "{student.get_name()}"', category='success')

        return redirect(url_for('students'))
    else:
        msg = get_message_from_form(form)
        if msg:
            flash(msg, category='danger')

    return render_template('edit_student.html', **locals())


@app.route('/delete_student/<int:id>', methods=['GET'])
@admin_required
def delete_student(id):
    db_sess = db_session.create_session()
    student = db_sess.query(Student).filter(Student.id == id).first()
    if not student:
        flash('No such student', category='danger')
    else:
        flash(f'Successfully deleted student "{student.get_name()}"', category='success')
        db_sess.delete(student)
        db_sess.commit()
    return redirect(url_for('students'))


@app.route('/add_student', methods=['GET', 'POST'])
@admin_required
def add_student():
    db_sess = db_session.create_session()
    form = SubmitStudentForm()
    sex = Student.get_sex_choices()
    if form.validate_on_submit():
        student = db_sess.query(Student).filter(func.lower(Student.last_name) == func.lower(form.last_name.data)). \
            filter(func.lower(Student.first_name) == func.lower(form.first_name.data)).first()
        if student:
            flash('Student with such last name and first name already exists', category='danger')
            return render_template('add_student.html', **locals())

        student = Student()
        student.n_class = form.n_class.data
        student.middle_name = form.middle_name.data
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.birthday = form.birthday.data
        student.sex = sex.index(form.sex.data)
        student.study = form.study.data
        db_sess.add(student)
        flash(f'Successfully added student "{student.get_name()}"', category='success')
        db_sess.commit()
        return redirect(url_for('students'))
    else:
        msg = get_message_from_form(form)
        if msg:
            flash(msg, category='danger')

    return render_template('add_student.html', **locals())
