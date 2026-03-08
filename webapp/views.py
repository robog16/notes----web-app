from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
from datetime import datetime
import json




views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':


        title = request.form.get('title')
        content = request.form.get('content')
        # date = datetime.now().strftime('%Y-%m-%d %H:%M')

        if len(title) < 1:
            flash('Title is too short!', category = 'error')
        elif len(title) < 1:
            flash('Note is too short!', category = 'error')
        else:
            new_note = Note(title = title, content = content, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('New note added!', category = 'success')
        
    return render_template('home.html', user = current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note_id = json.loads(request.data)['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({}) 
    return jsonify({}), 400  