from flask import render_template, redirect, session, flash, url_for, request
from .models import User
from app import db
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from app.models import Habit, Completion


def register_routes(app):
    @app.route('/')
    def index():
        return render_template("home.html", email=session.get("email"))
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if session.get('email') != None:
            return redirect(url_for('index'))

        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            # Check if the email already exists in the database
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email is already registered. Please log in.', 'danger')
                return redirect(url_for('login'))

            # Save new user to the database
            user = User(email=email, password=password)
            db.session.add(user)
            db.session.commit()

            flash('Account created successfully. Please log in.', 'success')
            return redirect(url_for('login'))

        return render_template('signup.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if session.get('email') != None:
            return redirect(url_for('index'))
            
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            # Query user from the database
            user = User.query.filter_by(email=email).first()
            if user and user.password == password:
                session['email'] = user.email
                flash('Logged in successfully.', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid email or password.', 'danger')

        return render_template('login.html')

    @app.route('/logout', methods=['POST'])
    def logout():
        session.clear()
        flash('Logged out successfully.', 'success')
        return redirect(url_for('index'))

    # For errors
    @app.errorhandler(404)
    def page_not_found(e):
        """Handle 404 errors"""
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        """Handle 500 errors"""
        return render_template('500.html'), 500
