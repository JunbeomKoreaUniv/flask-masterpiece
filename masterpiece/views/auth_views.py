from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from masterpiece import db

from masterpiece.forms import UserCreateForm, UserLoginForm
from masterpiece.models import User

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/create/', methods=('GET', 'POST'))
def create():
    form = UserCreateForm()
    if request.method=='POST' and form.validate_on_submit():
        user = User.query.filter_by(user_name=form.user_name.data).first()
        user_id = User.query.filter_by(user_email_id=form.user_email_id.data).first()
        if not user and not user_id:
            user = User(user_email_id=form.user_email_id.data, user_name=form.user_name.data, password=generate_password_hash(form.password1.data))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        elif user and not user_id:
            flash('이미 존재하는 사용자명입니다.')
        elif not user and user_id:
            flash('이미 존재하는 아이디입니다.')
        else:
            flash('이미 존재하는 사용자명이며 아이디입니다')
    return render_template('auth_create.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(user_email_id=form.user_email_id.data).first()
        if not user:
            flash('존재하지 않는 ID입니다')
        elif not check_password_hash(user.password, form.password.data):
            flash('ID는 존재하나 비밀번호가 일치하지 않습니다')
        else:
            session.clear()
            session['user_id'] = user.id
            _next = request.args.get('next', '')
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for('main.index'))
    return render_template('auth_login.html', form=form)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)
    return wrapped_view