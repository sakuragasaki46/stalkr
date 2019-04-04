from flask import (
    Blueprint, abort, flash, redirect, render_template, request, url_for)
import db
import re
import datetime

bp = Blueprint('s', __name__, url_prefix='/s')

def slugify(s):
    return re.sub('[^A-Za-z0-9]+', '-', s).strip('-').title()

def canonical_person_slug(id):
    p = db.S_Person[id]
    return slugify(p.first_name) + '-' + slugify(p.last_name)

def person_from_form():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    birthday_y = request.form.get('birthday_y')
    birthday_m = request.form.get('birthday_m')
    birthday_d = request.form.get('birthday_d')
    try:
        birthday = datetime.date(int(birthday_y), int(birthday_m), int(birthday_d))
    except (TypeError, ValueError):
        birthday = None
    return dict(first_name=first_name, last_name=last_name,
                birthday=birthday)

@bp.route('/<slug:slug>-<int:id>/')
@bp.route('/<int:id>/')
def detail(id, slug=None):
    try:
        canonical_slug = canonical_person_slug(id)
        if canonical_slug != slug:
            return redirect(url_for('.detail', id=id, slug=canonical_slug))
    except db.S_Person.DoesNotExist:
        abort(404)
    return render_template('detail.html', p=db.S_Person[id])

@bp.route('/<slug:slug>-<int:id>/edit', methods=['GET', 'POST'])
@bp.route('/<int:id>/edit')
def detail_edit(id, slug=None):
    try:
        canonical_slug = canonical_person_slug(id)
        if canonical_slug != slug:
            return redirect(url_for('.detail_edit', id=id, slug=canonical_slug))
    except db.S_Person.DoesNotExist:
        abort(404)
    if request.method == 'POST':
        pj = person_from_form()
        db.S_Person.update(**pj).where(S_Person.id == id).execute()
        flash('Successfully updated')
    return render_template('detail-edit.html', p=db.S_Person[id])

@bp.route('/new/', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        pj = person_from_form()
        p = db.S_Person.create(**pj)
        flash('Successfully created')
        return redirect(canonical_person_slug(p.id) + '-' + str(p.id))
    return render_template('detail-edit.html', p=None)
