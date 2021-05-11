import os

from flask import render_template, redirect, flash, url_for, send_from_directory, request
import xlsxwriter
from werkzeug.exceptions import abort

from data import db_session
from data.file import File
from data.level import Level
from data.olympiad import Olympiad
from data.result import Result
from data.student import Student
from data.user import User
from forms.report import ReportForm
from global_app import get_app, get_dir
from utils.permissions_required import teacher_required, admin_required

app = get_app()
current_user: User


@app.route('/report', methods=['GET', 'POST'])
@teacher_required
def report():
    db_sess = db_session.create_session()
    form = ReportForm()
    levels = {str(i.id): i for i in db_sess.query(Level).all()}
    form.level.choices = [('', '')] + [(str(k), v.name) for k, v in levels.items()]
    olympiad_names = [i[0] for i in db_sess.query(Olympiad.name).distinct().all()]
    form.olympiad.choices = [''] + olympiad_names

    results = db_sess.query(Result).join(Olympiad).join(Student)
    if form.validate_on_submit():
        if form.last_name.data:
            results = results.filter(Student.last_name.like(f'%{form.last_name.data}%'))
        if form.n_class.data:
            results = results.filter(Result.n_class == form.n_class.data)
        if form.olympiad.data:
            results = results.filter(Olympiad.name.like(f'%{form.olympiad.data}%'))
        if form.level.data:
            results = results.filter(Olympiad.level_id == levels[form.level.data].id)

        if request.form.get('apply'):
            ...
        elif request.form.get('get_report'):
            return get_report(db_sess, results)

    results = results.all()
    return render_template('report.html', **locals())


def get_report(db_sess, query):
    file = File()
    file.extension = 'xlsx'
    db_sess.add(file)
    db_sess.commit()
    base = os.path.join(get_dir(), 'files', 'report')
    filename = os.path.join(base, file.get_name())
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet(name='Олимпиада')
    head = ['№', 'Предмет', 'Уровень', 'Класс', 'Дата', 'Фамилия',
            'Имя', 'Отчество', 'Место', 'Ранг', 'Балл']
    worksheet.write_row(0, 0, head)
    for i, result in enumerate(query.all()):
        row = [
            i + 1,
            result.olympiad.name,
            result.olympiad.level.name,
            result.n_class,
            result.date.strftime('%d.%m.') + str(result.date.year).rjust(4, '0'),
            result.student.last_name,
            result.student.first_name,
            (result.student.middle_name if result.student.middle_name else ''),
            result.place,
            (result.level.name if result.level else ''),
            result.points
        ]
        worksheet.write_row(i + 1, 0, row)
    workbook.close()
    return redirect(url_for('download_report', id=file.id))


@app.route('/report/<int:id>', methods=['GET'])
@teacher_required
def download_report(id):
    db_sess = db_session.create_session()
    report = db_sess.query(File).filter(File.id == id).first()
    if not report:
        abort(404)
    base = os.path.join(get_dir(), 'files', 'report')
    return send_from_directory(
        directory=base, filename=report.get_name(),
        as_attachment=True, attachment_filename='report_' + report.get_name())
