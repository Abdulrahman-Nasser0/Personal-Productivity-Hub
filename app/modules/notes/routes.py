from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Note, User

notes_bp = Blueprint('notes', __name__, url_prefix='/notes')

@notes_bp.route('/')
def index():

    user_email = session.get('email')  
    if user_email:
        user = User.query.filter_by(email=user_email).first()
        if user:
            notes = Note.query.filter_by(user_id=user.id).all() 
        else:
            notes = [] 
    else:
        return redirect(url_for('login'))

    return render_template('notes/index.html', notes=notes)

@notes_bp.route('/create', methods=['POST'])
def create():
    """Create a new note"""
    title = request.form.get('title')
    content = request.form.get('content')
    user_email = session.get('email')  

    if title and content and user_email:
        user = User.query.filter_by(email=user_email).first()
        if user:
            note = Note(title=title, content=content, user_id=user.id)  
            db.session.add(note)
            db.session.commit()
            flash('Note created successfully!', 'success')
        else:
            flash('User not found. Please log in again.', 'danger')
    else:
        flash('Invalid input. Please try again.', 'danger')

    return redirect(url_for('notes.index'))


@notes_bp.route('/view/<int:note_id>')
def view(note_id):
    """View a specific note's content"""
    user_email = session.get('email')  
    if not user_email:
        flash('You must be logged in to view this note.', 'danger')
        return redirect(url_for('login'))

    user = User.query.filter_by(email=user_email).first()
    if not user:
        flash('User not found. Please log in again.', 'danger')
        return redirect(url_for('login'))

    note = Note.query.filter_by(id=note_id, user_id=user.id).first_or_404()
    return render_template('notes/view.html', note=note)

@notes_bp.route('/delete/<int:note_id>', methods=['POST'])
def delete(note_id):
    """Delete a specific note"""
    user_email = session.get('email')  
    if not user_email:
        flash('You must be logged in to delete a note.', 'danger')
        return redirect(url_for('login'))

    user = User.query.filter_by(email=user_email).first()
    if not user:
        flash('User not found. Please log in again.', 'danger')
        return redirect(url_for('login'))

    note = Note.query.filter_by(id=note_id, user_id=user.id).first()
    if note:
        db.session.delete(note)
        db.session.commit()
        flash('Note deleted successfully.', 'success')
    else:
        flash('Note not found or you do not have permission to delete it.', 'danger')

    return redirect(url_for('notes.index'))