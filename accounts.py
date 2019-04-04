import functools
from flask import Blueprint, redirect, render_template session, url_for

def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('accounts.login'))
        return func(*args, **kwargs)
    return wrapper

bp = Blueprint('accounts', __name__)

@bp.route('/login/')
def login():
    return render_template('login.html')
