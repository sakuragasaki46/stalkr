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

def do_client_auth(username, password):
    try:
        user = db.User.get(db.User.username == username)
    except db.User.DoesNotExist:
        return 'No user called %r exists.' % username
    if not check_password_hash(user.password, password):
        return 'Incorrect password.'
    return 'ok'

bp = Blueprint('accounts', __name__, url_prefix='/accounts')

@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        message = do_client_auth(request.form.get('username'), request.form.get('password'))
        if message == 'ok':
            returnto = request.args.get('returnto', '/')
            return redirect(returnto)
        else:
            flash(message)
    return render_template('login.html')
