from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Import Flask-Migrate
import os

db = SQLAlchemy()
migrate = Migrate()  # Initialize Flask-Migrate

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    app.config['SECRET_KEY'] = 'xyz' 
   
    db.init_app(app)
    migrate.init_app(app, db)  

    # Register blueprints
    from app.modules.habits import habits_bp
    from app.modules.todos import todos_bp
    
    app.register_blueprint(habits_bp)
    app.register_blueprint(todos_bp)

    # Register main routes
    from app import routes
    
    return app
