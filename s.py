from flask import Blueprint, abort, redirect, render_template, url_for
import db
import re

bp = Blueprint('s', __name__, url_prefix='/s')

def slugify(s):
    return re.sub('[^A-Z0-9]+', '-', s).strip('-').title()

def canonical_person_slug(id):
    p = db.S_Person[id]
    return slugify(p.first_name) + '-' + slugify(p.last_name)

@bp.route('/<slug:slug>-<int:id>/')
@bp.route('/<int:id>/')
def detail(id, slug=None):
    try:
        canonical_slug = canonical_person_slug(id)
        if canonical_slug != slug:
            return redirect(url_for('.detail', id=id, slug=canonical_slug))
    except db.S_Person.DoesNotExist:
        abort(404)
    return render_template('detail.html')

@bp.route('/<slug:slug>-<int:id>/edit')
@bp.route('/<int:id>/edit')
def detail_edit(id, slug=None):
    try:
        canonical_slug = canonical_person_slug(id)
        if canonical_slug != slug:
            return redirect(url_for('.detail_edit', id=id, slug=canonical_slug))
    except db.S_Person.DoesNotExist:
        abort(404)
    return render_template('detail.html')
