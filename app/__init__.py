from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  
import os

db = SQLAlchemy()
migrate = Migrate()  

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SECRET_KEY'] = 'xyz' 
   
    db.init_app(app)
    migrate.init_app(app, db)  

    # register blueprints
    from app.modules.habits import habits_bp
    from app.modules.todos import todos_bp
    from app.modules.notes import notes_bp
    
    app.register_blueprint(habits_bp)
    app.register_blueprint(todos_bp)
    app.register_blueprint(notes_bp)

    # register main routes
    from app import routes
    
    return app
