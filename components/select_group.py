from flask import render_template, redirect, flash, request
from flask_login import login_required, current_user

from data import db_session
from data.user import User

from global_app import get_app
from utils.permissions_required import teacher_required

app = get_app()
current_user: User


@app.route('/select_group', methods=['GET', 'POST'])
@teacher_required
def select_group():
    db_sess = db_session.create_session()
    _return = request.args.get('return', default='', type=str)
    groups = current_user.group
    return render_template('select_group.html', **locals())
