from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Task, User

todos_bp = Blueprint('todos', __name__, url_prefix='/todos')

@todos_bp.route('/')
def index():
    user_email = session.get('email') 
    if user_email:
        user = User.query.filter_by(email=user_email).first()
        if user:
            tasks = Task.query.filter_by(user_id=user.id).all()
            return render_template('todos/index.html', tasks=tasks)
    return redirect(url_for('login'))


@todos_bp.route('/create', methods=['POST'])
def create():
    title = request.form.get('title')
    user_email = session.get('email') 
    if title and user_email:
        user = User.query.filter_by(email=user_email).first()
        if user:
            task = Task(title=title, completed=False, user_id=user.id)
            db.session.add(task)
            db.session.commit()
    return redirect(url_for('todos.index'))


@todos_bp.route('/complete/<int:task_id>', methods=['POST'])
def complete(task_id):
    task = Task.query.get(task_id)
    task.completed = not task.completed #toggle
    db.session.commit()
    return redirect(url_for('todos.index'))
    
@todos_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    """Delete a specific task"""
    user_email = session.get('email')  
    if not user_email:
        flash('You must be logged in to delete a task.', 'danger')
        return redirect(url_for('login'))

    user = User.query.filter_by(email=user_email).first()
    if not user:
        flash('User not found. Please log in again.', 'danger')
        return redirect(url_for('login'))

    task = Task.query.filter_by(id=task_id, user_id=user.id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully.', 'success')
    else:
        flash('Task not found or you do not have permission to delete it.', 'danger')

    return redirect(url_for('todos.index'))