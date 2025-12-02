# app/__init__.py
from flask import Flask, redirect, url_for
from app.config import config
import os


def create_app(config_name=None):
    """Application factory function"""
    
    # Determine configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    cfg = config.get(config_name, config['default'])
    
    # Create Flask app
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(cfg)
    
    # Register blueprints
    from app.routes.students import students_bp
    from app.routes.instructors import instructors_bp
    from app.routes.courses import courses_bp
    
    app.register_blueprint(students_bp)
    app.register_blueprint(instructors_bp)
    app.register_blueprint(courses_bp)
    
    # Home route
    @app.route('/')
    def home():
        return redirect(url_for('students.list'))
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return {'error': 'Page not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return {'error': 'Internal server error'}, 500
    
    return app
