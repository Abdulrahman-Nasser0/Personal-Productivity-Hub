from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Habit, Completion, User
from datetime import datetime, timedelta

habits_bp = Blueprint('habits', __name__, url_prefix='/habits')

@habits_bp.route('/')
def index():
    user_email = session.get('email')
    if user_email:
        user = User.query.filter_by(email=user_email).first()
        if user:
            habits = Habit.query.filter_by(user_id=user.id).all()
        else:
            habits = []  
    else:
        return redirect(url_for('login'))  
    
    today = datetime.utcnow().date()
    for habit in habits:
        completion = Completion.query.filter_by(
            habit_id=habit.id, 
            completion_date=today
        ).first()
        habit.completed_today = completion is not None
    
    return render_template('habits/index.html', habits=habits)

@habits_bp.route('/create', methods=['POST'])
def create():
    name = request.form.get('name')
    user_email = session.get('email') 
    if name and user_email:
        user = User.query.filter_by(email=user_email).first()
        if user:
            habit = Habit(name=name, user_id=user.id)  
            db.session.add(habit)
            db.session.commit()
            flash('Habit created successfully!', 'success')
        else:
            flash('User not found. Please log in again.', 'danger')
    else:
        flash('Invalid input. Please try again.', 'danger')
    return redirect(url_for('habits.index'))

@habits_bp.route('/complete/<int:habit_id>', methods=['POST'])
def complete(habit_id):
    """Mark a habit as complete for the current day"""
    habit = Habit.query.get_or_404(habit_id)
    today = datetime.utcnow().date()
    
   
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
    """Display a calendar of habit completion history"""
    user_email = session.get('email')  
    if user_email:
        user = User.query.filter_by(email=user_email).first()
        if user:
            habits = Habit.query.filter_by(user_id=user.id).all() 
        else:
            habits = []  
    else:
        habits = []  

    today = datetime.utcnow().date()
    days = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
    
    for habit in habits:
        completions = Completion.query.filter(
            Completion.habit_id == habit.id,
            Completion.completion_date >= days[0],
            Completion.completion_date <= days[-1]
        ).all()
        
        habit.completion_dates = [c.completion_date.strftime('%Y-%m-%d') for c in completions]
    
    return render_template('habits/calendar.html', habits=habits, days=days)
