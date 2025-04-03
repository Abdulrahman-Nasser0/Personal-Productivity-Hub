from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    app.config['SECRET_KEY'] = 'xyz' 
   
    db.init_app(app)

    

    # Register main routes
    from app import routes
    
    return app
