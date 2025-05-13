from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Note, User

notes_bp = Blueprint('notes', __name__, url_prefix='/notes')

@notes_bp.route('/')
def index():
    """Display notes for the logged-in user and a form to create a new note"""
    user_email = session.get('email')  # Get the logged-in user's email
    if user_email:
        user = User.query.filter_by(email=user_email).first()
        if user:
            notes = Note.query.filter_by(user_id=user.id).all()  # Filter notes by user_id
        else:
            notes = []  # No user found
    else:
        notes = []  # No email in session

    return render_template('notes/index.html', notes=notes)

@notes_bp.route('/create', methods=['POST'])
def create():
    """Create a new note"""
    title = request.form.get('title')
    content = request.form.get('content')
    user_email = session.get('email')  # Get the logged-in user's email

    if title and content and user_email:
        user = User.query.filter_by(email=user_email).first()
        if user:
            note = Note(title=title, content=content, user_id=user.id)  # Link note to user
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
    note = Note.query.get_or_404(note_id)
    return render_template('notes/view.html', note=note)
