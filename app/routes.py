from flask import render_template, redirect, url_for

def register_routes(app):
    @app.route('/')
    def index():
        #Main page 
        return redirect(url_for('habits.index'))
    
    
    # For errors
    @app.errorhandler(404)
    def page_not_found(e):
        """Handle 404 errors"""
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        """Handle 500 errors"""
        return render_template('500.html'), 500
