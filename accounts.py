import functools
from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for)
import db
from werkzeug.security import check_password_hash, generate_password_hash

def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('accounts.login'))
        return func(*args, **kwargs)
    return wrapper

bp = Blueprint('accounts', __name__, url_prefix='/accounts')

@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        message = None
        try:
            user = db.User.get(db.User.username == username)
        except db.User.DoesNotExist:
            message = 'No user called %r exists.' % username
        if not check_password_hash(user.password, password):
            message = 'Incorrect password.'
        if not message:
            session['user_id'] = user.id
            returnto = request.args.get('returnto', '/')
            return redirect(returnto)
        else:
            flash(message)
    return render_template('login.html')

@bp.route('/create-2032/', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        message = None
        if password != confirm_password:
            message = 'Password mismatch.'
        try:
            user = db.User.create(username=username, password=generate_password_hash(password))
        except db.pw.IntegrityError:
            message = 'An user called %r already exists.' % username
        if not message:
            session['user_id'] = user.id
            returnto = request.args.get('returnto', '/')
            return redirect(returnto)
        else:
            flash(message)
    return render_template('create-account.html')
