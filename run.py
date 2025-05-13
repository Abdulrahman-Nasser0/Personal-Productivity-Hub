from app import create_app, db

app = create_app()

# register routes
from app.routes import register_routes
register_routes(app)

# create database 
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)