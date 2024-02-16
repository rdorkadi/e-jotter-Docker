# for url endpoints

from crypt import methods
from flask import Blueprint, flash, jsonify, render_template, request
from flask_login import login_required, logout_user, current_user
from .models import Note
from . import db
import json


# Creating a blueprint
# syntax: Blueprint(<name of the view>,__name__)
views = Blueprint('views', __name__)



# decorators
# for specifying the routes
@views.route('/', methods=['GET','POST'])
@views.route('/home', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        # notes that user typed in UI
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!',category='error')
        else:
            # adding the note to db
            new_note = Note(data=note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!',category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['note']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})