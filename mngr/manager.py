from typing_extensions import NotRequired
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
        ' t.name,'
        'FROM notes n, user u, tags t, tags_notes tn'
        ' WHERE n.userid = u.id AND t.id = tn.tags AND n.id = tn.notes'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('notes/index.html', notes=notes)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        tags = request.form['tags']
        error = None

        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO notes (title, body, userid)'
                ' VALUES (?, ?, ?)',(title, body, g.user['id'])
            )
            for tag in tags:
                db.execute(
                    'INSERT INTO tags (name)'
                    ' VALUES (?)',(tag)
                )
            db.commit()
            note_id = db.execute('SELECT id FROM notes'
            ' WHERE title = ? AND userid = ?',(title, g.user['id']))
            for tag in tags:
                tag_id = db.execute('SELECT id FROM tags'
                    ' WHERE name = ?',(tag,))
                db.execute(
                    'INSERT INTO tags_notes (notes, tags)'
                    ' VALUES (?, ?)',(note_id, tag_id)
                )
    	    db.commit()
            return redirect(url_for('manager.index'))
    return render_template('manager/create.html')
    
                
def get_note(id, check_author=True):
    note = get_db().execute(
        'SELECT n.id, n.userid, n.created, n.title, n.body,'
        ' u.id, u.username,'
        ' t.name,'
        'FROM notes n, user u, tags t, tags_notes tn'
        ' WHERE n.userid = u.id AND t.id = tn.tags AND n.id = tn.notes'
        'AND n.id = ?',(id,) 
    ).fetchone()
    if note is None:
        abort(404, f"Post id {id} doesn't exist.")
    if check_author and note['userid'] != g.user['id']:
        abort(403)
    return note