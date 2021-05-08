from flask import render_template, url_for, flash
from flask_login import login_required
from werkzeug.utils import redirect

from data import db_session
from data.student import Student
from global_app import get_app
from utils.permissions_required import teacher_required

app = get_app()


@app.route('/confirm_transfer', methods=['GET'])
@teacher_required
def confirm_transfer():
    db_sess = db_session.create_session()
    students = db_sess.query(Student).all()
    for i in students:
        i: Student
        i.n_class += 1
        if i.n_class > 11:
            i.n_class = 11
            i.study = False
    flash('Successfully transferred all students', category='success')
    db_sess.commit()
    return redirect(url_for('transfer'))


@app.route('/transfer', methods=['GET'])
@teacher_required
def transfer():
    db_sess = db_session.create_session()
    return render_template('transfer.html')
