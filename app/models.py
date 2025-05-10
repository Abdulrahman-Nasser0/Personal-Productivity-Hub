from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    habits = db.relationship('Habit', backref='user', lazy=True)  # One-to-many relationship
    tasks = db.relationship('Task', backref='user', lazy=True)
    def __repr__(self):
        return f'<User {self.email}>'


class Habit(db.Model):
    __tablename__ = 'habits'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to User
    completions = db.relationship('Completion', backref='habit', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Habit {self.name}>'

class Completion(db.Model):
    __tablename__ = 'completions'
    
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    completion_date = db.Column(db.Date, default=datetime.utcnow().date, nullable=False)
    
    def __repr__(self):
        return f'<Completion {self.habit_id} on {self.completion_date}>'

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to User

    def __repr__(self):
        return f'<Task {self.title}>'