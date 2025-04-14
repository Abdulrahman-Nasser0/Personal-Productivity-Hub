
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Habit, Completion
from datetime import datetime, timedelta

habits_bp = Blueprint('habits', __name__, url_prefix='/habits')

@habits_bp.route('/')
def index():
    # Display all habits and a form to create a new habit
    habits = Habit.query.all()
    
    # Check if each habit is completed today
    for habit in habits:
        today = datetime.utcnow().date()
        completion = Completion.query.filter_by(
            habit_id=habit.id, 
            completion_date=today
        ).first()
        habit.completed_today = completion is not None
    
    return render_template('habits/index.html', habits=habits)

@habits_bp.route('/create', methods=['POST'])
def create():
    # Create a new habit
    name = request.form.get('name')
    if name:
        habit = Habit(name=name)
        db.session.add(habit)
        db.session.commit()
    return redirect(url_for('habits.index'))

@habits_bp.route('/complete/<int:habit_id>', methods=['POST'])
def complete(habit_id):
    """Mark a habit as complete for the current day"""
    habit = Habit.query.get_or_404(habit_id)
    today = datetime.utcnow().date()
    
    # Check if already completed today
    existing_completion = Completion.query.filter_by(
        habit_id=habit_id, 
        completion_date=today
    ).first()
    
    if not existing_completion:
        completion = Completion(habit_id=habit_id, completion_date=today)
        db.session.add(completion)
        db.session.commit()
    
    return redirect(url_for('habits.index'))






@habits_bp.route('/calendar')
def calendar():
    return render_template('habits/calendar.html', habits=habits, days=days)
