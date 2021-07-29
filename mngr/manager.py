
from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from mngr.auth import login_required
from mngr.auth import get_db

bp = Blueprint('manager', __name__)


@bp.route('/')
def index():
    db = get_db()
    notes = db.execute(
        'SELECT n.id, n.userid, n.created, n.title, n.body,'
        ' u.id, u.username,'
        ' t.tag, t.id,'
        ' tn.notes, tn.tags' 
        ' FROM notes n, user u, tags t, tags_notes tn'
        ' WHERE n.userid = u.id AND tn.notes=n.id AND tn.tags=t.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('manager/index.html', notes=notes)

@bp.route('/<title>')
def noteview(title):
    db = get_db()
    notes = db.execute(
        'SELECT n.id, n.userid, n.created, n.title, n.body,'
        ' u.id, u.username,'
        ' t.tag, t.id,'
        ' tn.notes, tn.tags' 
        ' FROM notes n, user u, tags t, tags_notes tn'
        ' WHERE n.userid = u.id AND tn.notes=n.id AND tn.tags=t.id AND n.title = ?',(title,)
    ).fetchall()
    return render_template('manager/view.html', notes=notes)


@bp.route('/tagview/<tag>')
def tagfilter(tag):
    db = get_db()
    notes = db.execute(
        'SELECT n.id, n.userid, n.created, n.title, n.body,'
        ' u.id, u.username,'
        ' t.tag, t.id,'
        ' tn.notes, tn.tags' 
        ' FROM notes n, user u, tags t, tags_notes tn'
        ' WHERE t.tag = ? AND n.userid = u.id AND tn.notes=n.id AND tn.tags=t.id'
        ' ORDER BY created DESC',(tag,)
    ).fetchall()
    return render_template('manager/tagview.html', notes=notes, tag=tag)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    tags = request.form.get('tags')
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        db = get_db()
        title_test = db.execute('SELECT * FROM notes WHERE title = ?',(title,)).fetchall()
        if title_test:
            error= 'Title Already exists.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO notes (title, body, userid)'
                'VALUES(?, ?, ?)',(title, body, g.user['id'])
            )
            note_id = db.execute(
                'SELECT id FROM notes WHERE title=?',(title,)
            ).fetchone()
            db.commit()
            db.execute(
                'INSERT INTO tags_notes (notes, tags)'
                'VALUES(?, ?)',(note_id[0], tags)
            )
            db.commit()
            return redirect(url_for('manager.index'))
    return render_template('manager/create.html')
    
                
def get_note(id, check_author=True):
    note = get_db().execute(
        'SELECT n.id, n.userid, n.created, n.title, n.body,'
        ' u.id, u.username '
        'FROM notes n, user u'
        ' WHERE n.userid = u.id '
        'AND n.id = ?',(id,) 
    ).fetchone()
    if note is None:
        abort(404, f"Post id {id} doesn't exist.")
    if check_author and note['userid'] != g.user['id']:
        abort(403)
    return note


@bp.route('/<int:id>/update', methods = ('GET', 'POST'))
@login_required
def update(id):
    note = get_note(id)
    tags = request.form.get('tags')
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        #tags = request.form['tags']
        error = None

        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute('UPDATE notes SET title = ?, body = ? WHERE id = ?',(title, body, id))
            db.commit()
            db.execute('UPDATE tags_notes SET tags = ? WHERE notes = ?',(tags, id))
            db.commit()
            return redirect(url_for('manager.index'))
    return render_template('manager/update.html', note = note)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_note(id)
    db = get_db()
    db.execute('DELETE FROM notes WHERE id = ?',(id,))
    db.commit()
    db.execute('DELETE FROM tags_notes WHERE notes = ?',(id,))
    db.commit()
    return redirect(url_for('manager.index'))