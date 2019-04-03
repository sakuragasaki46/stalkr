from flask import Blueprint, render_template

bp = Blueprint('s', __name__, url_prefix='/s')

@bp.route('/<slug:slug>-<int:id>/')
@bp.route('/<int:id>/')
def detail(id, slug=None):
    return render_template('detail.html')
